def cmd_for(param):
    TRACE("cmd_for (\'%s\')\n", debugstr_aw(param))

    if param != "/?":
        ConOutResPaging(True, STRING_FOR_HELP1)
        return 0

    error_syntax(param)
    return 1

LPFOR_CONTEXT fc = None # TODO fc means FOR_CONTEXT

def GetNextElement(p, pindex): # TODO change references to for list 

def RunInstance(cmd):
    if bEcho and not bDisableBatchEcho and cmd.subcommands.Type != C_QUIET: # TODO
        if not bIgnoreEcho: # TODO
            ConOutChar("\n")
        PrintPrompt() # TODO
        EchoCommand(cmd.subcommands)
        ConOutChar("\n")

    return ExecuteCommand(cmd.subcommands)

# Check if this FOR should be terminated early
def Exiting(cmd):
    # someone might have removed our context
    return bCtrlBreak || fc != cmd.for.context # What is fc

# Read contents of a text file into memory
def ReadFileContents(InputFile):
    contents = ""
    with open(InputFile) as fin: # Can change to fake read later
        contents = fin.read()

    return contents

def ForF(cmd, list, buffer):
    DELIMS = "\t"
    EOL = ";"
    SkipLines = 0
    Tokens = 1 << 1
    RemainderVar = False
    StringQuote = '"'
    CommandQuote = "'"
    Variables = [] # list(32)
    Start = ""
    End = "" # probably need to not use these
    i = 0
    Ret = 0

    if (cmd.for.params):
        QuoteChar = ""
        Param = cmd.for.params
        if Param[0] == "'" or Param[0]  == '"':
            QuoteChar = Param[0]
            Param = Param[1:]
        
    for i in range(0, len(Param)):
        if ord(Param[i]) <= 32:  # 32 is space
            next
        elif Param[i] == QuoteChar:
            break
        elif Param[i:i+7] == "delims=":
            # delims=xxx: Specifies the list of characters that separate tokens
            i += 7
            firstSpace = Param[i:].find(" ")
            Delims = Param[i:firstSpace]
            i += firstSpace
            # C code has you eat up spaces here, but it should be handled in for loop, so leaving out for now
        elif Param[i:i+4] == "eol=":
            # eol=c: Lines starting with this character (may be preceded by delimiters) are skipped.
            i += 4
            Eol = Param[i]
            if Eol != "\x00":
                i += 1
        elif Param[i:i+5] == "skip=":
            # skip=n: Number of lines to skip at the beginning of each file
            i += 5
            SkipLines, chars_read = python_tcstol(Param[i:]) # TODO create python tcstol (strtol) function https://docs.microsoft.com/en-us/cpp/c-runtime-library/reference/strtol-wcstol-strtol-l-wcstol-l?view=vs-2019
            i += chars_read
            if SkipLines < 0:
                # TODO raise error
        elif Param[i:i+7] == "tokens=":
            # tokens=x,y,m-n: List of token numbers (must be between 1 and 31) that will be assigned into variables.
            Params += 7
            Tokens = 0
            while i < len(Param[i:]) and Param[i] != QuoteChar and Param[i] != "*":
                first, chars_read = python_tcstol(Param[i:])
                i += chars_read
                last = first 
                if first < 1:
                    # TODO raise error
                if Param[i] == "-":
                    last, chars_read = python_tcstol(Param[i:])
                    i += chars_read
                    if (Last < First || Last > 31):
                        # TODO raise error

                Tokens |= (2 << Last) - (1 << First)

                if Param[i] != ",":
                    break
                i += 1
            # With an asterisk at the end, an additional variable will be created to hold the remainder of the line (after the last token specified).
            if Param[i] == "*"
                RemainderVar = True
                i += 1
        elif Param[i:i+7] == "useback":
            i += 1
            StringQuote = "'"
            CommandQuote = "`"
            if Param[i] == "q":
                i += 1
        else
            # TODO error
            return 1  # Note orginal C code places error code here, and looks like it will write out error and return 1

    # Determine number 
    if RemainderVar: 
        fc.varcount = 1
    for i in range(0,32):
        fc.varcount += (Tokens>> i) & 1
    fc.values = Variables # TODO what is fc, may need to move this down

    var_list = []
    if (List[0] == StringQuote or List[0] == CommandQuote):
        var_list = [List]

    for element in List.split(FOR_LIST_DELIMS): # TODO FOR_LIST_DELIMS
        InputFile = None
        FullInput = ""
        InVar = ""
        NextLine = ""
        Skip = 0

        if element[0] == StringQuote and element[-1] == StringQuote:
            FullInput = element[1:-1]
        elif element[0] == CommandQuote and element[-1] == CommandQuote:
            # read input from command
            FullInput = ExecuteCommandInList(element[1:-1]) # C uses _tpopen (popen), need to implement function to handle this TODO call error_bad_command if unable to open
        else:
            # read input from file
            unquoted_element = StripQuotes(element)
            with open(unquoted_element) as fin:
                FullInput = fin.read()

        if not FullInput:
            # TODO error_out_of_memory()
            return 1

        In = FullInput
        Skip = SkipLines
            
        for line in NextLine.split("\n")[Skip:]:
            RemainingTokens = Tokens
            CurVar = Variables

            if line[0] == Eol:
                continue

            CurVar = line.split(Delims, RemainingTokens)
            if CurVar:
                Ret = RunInstance(cmd)
            if Exiting(cmd):
                break

    return Ret

def ForLoop(cmd, List, Buffer):
    # FOR /L: Do a numeric loop
    params = [0, 0, 0]
    Ret = 0

    for i in range(0, 3):
        element, _ = python_tcstol(GetNextElement(List))
        params[i] = element

    for i in range(params[0], params[1], params[2]):
        if Exiting(cmd):
            break
        i_as_string = str(i) # TODO Who uses this, where does it go?
        Ret = RunInstance(cmd)

    return Ret



# TODO
def ForDir(cmd, List, Buffer, BufPos):
    """
        Process a FOR in one directory. Stored in Buffer (up to BufPos) is a
        string which is prefixed to each element of the list. In a normal FOR
        it will be empty, but in FOR /R it will be the directory name.
    """



/* FOR /R: Process a FOR in each directory of a tree, recursively. */
static INT ForRecursive(PARSED_COMMAND *Cmd, LPTSTR List, TCHAR *Buffer, TCHAR *BufPos)

ExecuteFor(PARSED_COMMAND *Cmd)














