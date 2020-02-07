# Need to make an if class or something to handle this 
# TODO Need IF Flags
# String compare
# Trace
# delay expansion
# console print


def GenericCmp(left, right):
    try:
        nLeft = int(left)
        try: 
            nRight = int(right)
            return -1 if nLeft < nRight else nLeft > nRight
        except:
            pass
    except: # Should find better way than this
        pass
    return StringCmp(left, right)  # TODO, functon 

def cmd_if(param):
    TRACE("cmd_if: (\'%s\')\n" % debugstr_aw(param))  # TODO
    if (param != "/?"):
        ConOutResPaging(True, STRING_IF_HELP1) #TODO
        return 0

    error_syntax(param) #TODO need function that returns int like C's strcmp()
    return 1


def ExecuteIf(parsed_command):
    result = false
    param = ""
    left = None
    right = None

    if (cmd.if.leftArg):  # TODO make cmd class
        left = DoDelayedExpansion(cmd.if.leftArg)
    
    right = DoDelayedExpansion(cmd.if.rightArg)

    if (not left and not right):
        return 1

    if cmd.if.operator == IF_CMDEXTVERSION:  # TODO
        # Check if cmd version is greater than n
        try:
            n = int(right)
            result = (2 >= n)
        except:
            error_syntax(right)
            # DO WE NEED cmd_free(right) or something similar?, maybe set it as None
            return 1
    elif cmd.if.operator == IF_DEFINED:
        # Checks if env var exists
        result = GetEnvVarOrSpecial(right) != None  # TODO
    elif cmd.if.operator == IF_ERRORLEVEL:
        # Checks if last exit code is greater or equal to n
        try:
            n = int(right)
            result = nEroorLevel >= n  # TODO
        except:
            error_syntax(right)
            # DO WE NEED cmd_free(right) or something similar?, maybe set it as None
            return 1
    elif cmd.if.operator == IF_EXIST:
        isDir = False
        size = 0
        # WIN32_FIND_DATA f  # TODO
        # HANDLE hFind  # TODO

        StripQuotes(right)  # TODO
        size = len(right)
        IsDir = right[-1] == "\\"
        if IsDir:
            right = right[:-1]

        hFind = FindFirstFile(right, f) # TODO
        if hFind != INVALID_HANDLE_VALUE:  # TODO
            if isDir
                result = ( (f.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) == FILE_ATTRIBUTE_DIRECTORY)  # TODO
            else:
                result = True
        if IsDir:
            right += "\\" # Probably better way to do that
    else:
        # case-insensitive string comp if /I 
        if cmd.if.flags & IFFLAG_IGNORECASE:
            left = left.lower()
            right = right.lower()

        if cmd.if.operator == IF_STRINGEQ:
            result = StringCmp(left, right) == 0
        else:
            result = GenericCmp(left, right)
            if cmd.if.operator == IF_EQU:
                result = (result == 0)
            if cmd.if.operator == IF_NEQ:
                result = (result != 0)
            if cmd.if.operator == IF_LSS:
                result = (result < 0)
            if cmd.if.operator == IF_LEQ:
                result = (result <= 0)
            if cmd.if.operator == IF_GTR:
                result = (result > 0)
            if cmd.if.operator == IF_GEQ:
                result = (result >= 0)

    if (result ^ ((cmd.if.flags & IFFLAG_NEGATE) != 0) ):
        return ExecuteCommand(cmd.subCommands)
    else:
        if cmd.subCommands.next
            return ExecuteCommand(cmd.subcommads.next)
        return 0







