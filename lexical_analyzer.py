charClass = 0
lexeme = 'a'
nextChar = 'a'
lexLen = 0
token = 0
nextToken = 0
charPos = 0

EOF = None
LETTER, DIGIT, UNKNOWN = 0, 1, 99

# TOKEN CODES
INT_LIT = 10
IDENT = 11
ASSIGN_OP = 20
ADD_OP = 21
SUB_OP = 22
MULT_OP = 23
DIV_OP = 24
LEFT_PAREN = 25
RIGHT_PAREN = 26
SEMICOLON = 27
EQUAL_SIGN = 28
ELIF_CODE = 29

FOR_CODE = 30
IF_CODE = 31
ELSE_CODE = 32
WHILE_CODE = 33
DO_CODE = 34
INT_CODE = 35
FLOAT_CODE = 36
SWITCH_CODE = 37
PRINT_OUTPUT = 38
QUOTE_CODE = 39
IN_CODE = 40
RANGE_CODE = 41


in_fp = open("front.in", "r")
txtdata = in_fp.read()
N = len(txtdata)


# lookUp
def lookup(ch):
    global nextToken
    if ch == '(':
        addChar()
        nextToken = LEFT_PAREN
    elif ch == ')':
        addChar()
        nextToken = RIGHT_PAREN
    elif ch == '+':
        addChar()
        nextToken = ADD_OP
    elif ch == '-':
        addChar()
        nextToken = SUB_OP
    elif ch == '*':
        addChar()
        nextToken = MULT_OP
    elif ch == '/':
        addChar()
        nextToken = DIV_OP
    elif ch == ':':
        addChar()
        nextToken = SEMICOLON
    elif ch == '=':
        addChar()
        nextToken = EQUAL_SIGN
    elif ch == '"':
        addChar()
        nextToken = QUOTE_CODE
    else:
        addChar()
        nextToken = EOF
    return nextToken


def addChar():
    global lexeme
    if lexLen <= 98:
        if lexeme == ' ':
            lexeme = nextChar
        else:
            lexeme = lexeme + nextChar
    else:
        print("Error - lexeme is too long")


def getChar():
    # A function that reads one character from the file and determines whether it is an alphabel
    # a number or something else.
    global charPos
    global nextChar
    global charClass

    if N > charPos:
        nextChar = txtdata[charPos]
        charPos = charPos + 1
    else:
        nextChar = EOF
        charPos = charPos + 1

    if nextChar != EOF:
        if nextChar.isalpha():
            charClass = LETTER
        elif nextChar.isdigit():
            charClass = DIGIT
        else:
            charClass = UNKNOWN
    else:
        charClass = EOF


def getNonBlank():
    if nextChar != EOF:
        while nextChar.isspace():
            getChar()


def lex():
    global lexeme
    global charClass
    global nextToken
    lexeme = ' '
    getNonBlank()
    if charClass == LETTER:
        addChar()
        getChar()
        while charClass == LETTER or charClass == DIGIT:
            addChar()
            getChar()
        if lexeme == 'for':
            nextToken = FOR_CODE
        elif lexeme == 'if':
            nextToken = IF_CODE
        elif lexeme == 'elif':
            nextToken = ELIF_CODE
        elif lexeme == 'else':
            nextToken = ELSE_CODE
        elif lexeme == 'while':
            nextToken = WHILE_CODE
        elif lexeme == 'do':
            nextToken = DO_CODE
        elif lexeme == 'int':
            nextToken = INT_CODE
        elif lexeme == 'float':
            nextToken = FLOAT_CODE
        elif lexeme == 'switch':
            nextToken = SWITCH_CODE
        elif lexeme == 'out':
            nextToken = PRINT_OUTPUT
        elif lexeme == 'in':
            nextToken = IN_CODE
        elif lexeme == 'range':
            nextToken = RANGE_CODE
        else:
            nextToken = IDENT
    elif charClass == DIGIT:
        addChar()
        getChar()
        while charClass == DIGIT:
            addChar()
            getChar()
        nextToken = INT_LIT
    elif charClass == UNKNOWN:
        lookup(nextChar)
        getChar()

    elif charClass == EOF:
        nextToken = EOF
        lexeme = 'EOF'
    print("Next token is:", nextToken, " next lexeme is", lexeme)
    return nextToken


"""
    PARSER FUNCTIONS START HERE
"""


def statement():
    # <statement> -> if_cond | print | for_loop_numbers | statement
    print("Start statement")
    if nextToken == IF_CODE or nextToken == ELIF_CODE or nextToken == ELSE_CODE:
        if_cond()
    elif nextToken == PRINT_OUTPUT:
        print_me()
    elif nextToken == FOR_CODE:
        for_loop()
    else:
        if nextToken != EOF:
            error()
        else:
            print("End Of File")
    print("End statement")


def print_me():
    """
    This function checks the syntax of the next 2 statements
    out(1), out("some dummy text")
    :return:
    """
    print("Start print me")
    lex()
    if nextToken != LEFT_PAREN:
        error()
    else:
        lex()
        # out(1)
        if nextToken == INT_LIT or nextToken == IDENT:  # can be also the content of a list for instance
            lex()
            if nextToken != RIGHT_PAREN:
                error()
            else:
                pass  # syntax is correct
        # out("some dummy text")
        elif nextToken == QUOTE_CODE:  # If the programmer wants to print a string
            lex()
            while nextToken != QUOTE_CODE:  # example = out("@one two three"), this check starts from @
                lex()
            else:
                lex()
                if nextToken != RIGHT_PAREN:
                    error()
        else:
            error()
    print("End print me")


def if_cond():
    print("Start if cond")
    condition, flag = [], True
    equal_check = ''  # this statement must be equal to == if not show an error
    """
        This Function behaves just like the if statement
        if condition:
            statement
        elif condition:
            statement
        else:
            statement
    """
    if nextToken != IF_CODE and nextToken != ELIF_CODE and nextToken != ELSE_CODE:
        error()
    else:
        if nextToken == ELSE_CODE:
            lex()
            if nextToken != SEMICOLON:
                error()
            else:
                lex()
                statement()
                flag = False
        if flag:
            lex()  # read the next token
            if nextToken == SEMICOLON:  # if it is semicolon, then show an error
                error()
            else:
                while nextToken != SEMICOLON:  # loop through the condition
                    if nextToken == EQUAL_SIGN:  # make sure we only have 2 equals
                        equal_check += '='
                    condition.append(nextToken)  # add the condition and pass the list to the function
                    lex()
                check_boolean_syntax(equal_check)  # if more than 2 equals than exit the script
                if boolexpr(condition):
                    pass
                if nextToken == ELIF_CODE:
                    equal_check, condition = '', []
                    while nextToken != SEMICOLON:  # loop through the condition
                        if nextToken == EQUAL_SIGN:  # make sure we only have 2 equals
                            equal_check += '='
                        condition.append(nextToken)
                        lex()
                        check_boolean_syntax(equal_check)  # if more than 2 equals than exit the script
                    if boolexpr(condition):  # call the condition boolean
                        pass  # call the statement function
    print("END if cond")


def for_loop():
    print("Start for loop numbers")
    """
        for i in range(number):
            <statement>
    """
    if nextToken == FOR_CODE:
        lex()
        if nextToken != IDENT:
            error()
        else:
            lex()
            if nextToken != IN_CODE:
                error()
            else:
                lex()
                if nextToken != RANGE_CODE:
                    error()
                else:
                    lex()
                    if nextToken != LEFT_PAREN:
                        error()
                    else:
                        lex()
                        if nextToken != INT_LIT:
                            error()
                        else:
                            lex()
                            if nextToken != RIGHT_PAREN:
                                error()
                            else:
                                lex()
                                if nextToken != SEMICOLON:
                                    lex()
                                else:
                                    pass
    else:
        error()
    print("END for loop numbers")


def check_boolean_syntax(equal_check):
    print("Start check_boolean_syntax")
    """
    :param equal_check:
    :return: if no syntax error was noticed, then the code will continue working
    """
    if not len(equal_check) == 2:
        if len(equal_check) == 1:
            print("Syntax Error: Perhaps you want to add another =?")
            exit()
        else:
            print(f"Syntax Error: Looks like you have {len(equal_check)} equals, "
                  f"You should remove {len(equal_check) - 2} equals!")
            exit()  # terminate the program

    print("END check_boolean_syntax")


def boolexpr(condition):
    print("Start Boolean")
    print("END Boolean")
    """
    A function to evaluate whether the condition is true or false
    :param condition:
    :return: True, Will always return True for now, We are just checking the syntax in this script
    """
    return True


def error():
    print("Syntax error: Invalid syntax")
    exit()


def main():
    if in_fp == None:
        print("ERROR - cannot open front.in ")
    else:
        getChar()
        while nextToken != EOF:
            lex()
            statement()
    in_fp.close()
    return 0



# <statement> -> <if_cond> | <for_loop> | <out>
# <if_cond> -> if <boolexpr>: <statement> [elif <boolexpr>: <statement>] [else: <statement>]
# <for_loop> -> for IDENT in range(INT_LIT): <statement>
# <boolexpr> -> INT_LIT | IDENT
# <out> -> ("{bool_exp}")

main()
