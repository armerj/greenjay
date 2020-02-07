class Cmd():
    bExit = False      #  /* Indicates EXIT was typed */
    bCanExit = True   #   /* Indicates if this shell is exitable */
    bCtrlBreak = False #  /* Ctrl-Break or Ctrl-C hit */
    bIgnoreEcho = False # /* Set this to TRUE to prevent a newline, when executing a command */
    fSingleCommand = 0 # /* When we are executing something passed on the command line after /C or /K */
    nErrorLevel = 0     # /* Errorlevel of last launched external program */
    bDisableBatchEcho = False
    bEnableExtensions = True
    bDelayedExpansion = False
    dwChildProcessId = 0
    batchContext = None  # refered in code as bc
    lpOriginalEnvironment 
    variables = {}
    ForContext = [] # list of forcontexts 
    """
    Below is from orginal C, I think we can use [ {<prev context>}, {"varcount" : 1, "variables" : {"a": 123} } ]
    typedef struct tagFORCONTEXT
{
    struct tagFORCONTEXT *prev;
    TCHAR firstvar;
    UINT   varcount;
    LPTSTR *values;
} FOR_CONTEXT, *LPFOR_CONTEXT;
    """

    implemented_commands = {"for": FORFUNC, "set": SETFUNC, "if": IFFUNC}

    def ParseCommandLine(self, cmd_line):
        parsed_command = self.ParseCommand(cmd_line)
        return ExecuteCommand(parsed_command)

    def ExecuteCommand():

    def GetEnvVarOrSpecial():

    def GetBatchVar():

    def SubstituteVars(cmd_line, delim):
        result = ""
        cmd_line_len = len(cmd_line)

        for i in range(0, cmd_line_len):
            if cmd_line[i] != delim:
                result += cmd_line[i]
                continue

            i += 1
            if batchContext and delim == "%":
                var, varnameLen = GetBatchVar(cmd_line[i:])
                if var:
                    result += var
                    i += varnameLen
                    continue

            # Find end of var name, ":" means end of name, and start optional modifier, except if followed immediately by delimiter
            endvarname = i
            while (cmd_line[endvarname] != delim and not (cmd_line[endvarname] == ":" and cmd_line[endvarname + 1] != delim) ):
                if endvarname >= cmd_line_len:
                    # TODO bad_subst
                endvarname += 1

            var = GetEnvVarOrSpecial(cmd_line[i:endvarname])
            if not var:
                # In a batch file, %NONEXISTENT% "expands" to an empty string
                if batchContext:
                    continue
                # TODO bad_subst
            varLength = len(var)

            if cmd_line[endvarname] == delim:
                # %var% - us as is
                result += var

            elif cmd_line[endvarname + 1] == "~":
                # %var:~[start][,length]% - substring, neg values start from end
                start_index, int_length = python_tcstol(cmd_line[endvarname + 2:]
                end_index = varLength
                i += int_length + 2

                if start_index < 0:
                    start_index += varLength
                start_index = max(start_index, 0) # if number is past beginning, set it to beginning
                start_index min(start_index, varLength) # if too far to right, set to end

                if cmd_line[i] == ",":
                    end_index, int_length = python_tcstol(cmd[i + 1])
                    i += int_length + 1
                    end_index += varLength if end_index < 0 else start_index
                    end_index = max(end_index, start_index)
                    end_index = min(end_index, varLength)

                if cmd_line[i] != delim:
                    # TODO bad_subst

                result += var[start_index:end_index]

            else:
                # %var:old=new% - replace all occurrences
                # %var:*old=new% - replace first occurence, drop everything before
		star = False

                if cmd_line[i] = "*":
                    star = True
                    i += 1
                
                equalsAt = cmd_line[i:].find("=")
                old = cmd_line[i:equalsAt]
                if len(old) == 0:
                    # TODO bad_subst
                i += equalsAt

               delimAt = cmd_line[i:].find(delim)
                new_str = cmd_line[i:delimAt]
                if len(new_str) == 0:
                    # TODO bad_subst
                i += delimAt

                while(len(var) > 0):
                    old_at_index = var.find(old)
                    if old_at_index == -1:
                        # no more occurances
                        result += var
                        break
                    if else:
                        # found occurance
                        if not star:
                            result += var[:old_at_index]
                            var = var[old_at_index + len(old)]
                        result += new_str

                        if star:
                            break



    def FindForVar(forVar, isParam0=False):
        # Search the list of FOR contexts for a variable
        for context in reversed(self.ForContext):  # traverse for contexts in reverse, likey since for var can overload previous var
            if forVar in context["variables"]:
                return context["variables"][forVar]

        return None
    

    def SubstituteForVars(cmd_line):
        result = ""

        for i in range(0, len(cmd_line)):
            if cmd_line[i] == "%":
                value = ""

                if cmd_line[i+1] = "~":
                    value = GetEnhancedVar(cmd_line[i+2], FindForVar)  # Should we be passing in Function, or is there a better method

                if not value:
                    value = FindForVar(cmd_line)

                if value:
                    if len(result) + len(value) > CMDLINE_LENGTH):
                        return False
                    result += value
                    i += 2
                    continue

            result += cmd_line[i]

        return result
                    

    def DoDelayedExpansion(cmd_line):
        buf1 = self.SubstituteForVars(cmd_line)
        if not buf1:
            return None

        if not self.bDelayedExpansion or buf1.find("!") < 0:
            return buf1

        return self.SubstituteVars(buf1, "!")


    def DoCommand(self, first, rest, parsed_command):
        full_command = first + rest
        special_char_index = 0
        param = ""
        nointernal = False
        ret = 0

        self.trace("Do Command: ('%s' '%s')\n" % first, rest)

        char_indexes = [first.find(i) for i in set("\t +,/;=[]")] # Check for each char in first
        special_char_index = min(filter(lambda x: x > -1, char_indexes)) # filter out -1, and then grap smallest number

        if "." in first[:special_char_index] or ":" in first[:special_char_index] or "\\" in first[: special_char_index]:
            nointernal = IsExistingFile(first[:special_char_index])

        if first in implemented_commands:
            param = first[special_char_index:] + rest
            if first != "echo":  # TODO Change all cmps to case insentive
                param = ltrim(param)

            return implemented_commands[first](param)

        return self.Execute(com, first, rest, parsed_command)


    def EchoCommand():

    def Unparse():

    def trace():


def IsExistingFile():



class Parsed_Command():
    subcommands = None
    next = None
    redirections = None
    type = 0
    command = {"rest": "", "first": []}
    if_struct = {"flags" : 0, "operator": 0, "leftArg" : "", "rightArg": ""}
    for_struct = {"switches": 0, "variable": "", "params":"", "list": "", "tagFORCONTEXT": None} # what is the tag for

