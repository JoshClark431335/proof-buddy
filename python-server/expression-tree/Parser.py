import string #no longer using re
from typing import List #used to create a type hint for a list of strings

#perhaps in future allow square brackets and braces. 
whitespace = ["\n","\t","\r"," "] #permits linebreak and indents for conditionals. all become \s in pre-processing step
arithSymbols = ["+","*","-"] # other math uses ascii, such as expt, quotient, remainder. Note: "/" not permitted
openGroupSymb = ["(","[","{"] # needed to separate open from closed for more precision with error messaging
closeGroupSymb = [")","]","}"] # possibly cond might be implemented one day with square brackets. presently, all these replaced by parens in pre-processing
specialChars = ["#","?","\u03BB","'"] #hashtag for bools,? for predicate suffix,unicode is for lambda (currently not in language), final item is single quote
AllowedChars = list(string.ascii_letters) + list(string.digits) + whitespace + arithSymbols + openGroupSymb + closeGroupSymb + specialChars
class Node:
    def __init__(self, children=[], parent=None, data='', name=None, tokenType=None, debug=False):
        self.children = children
        self.parent = parent
        self.data = data
        self.name = name
        self.type = tokenType
        self.debug = debug

    def __str__(self):
        # will print stuff if there is missing label or type information
        if (self.name == None or self.type == None) and self.debug:
            outStr = f'{self.children}, {self.data}'
            print(outStr)
        if self.debug:
            ans = self.name # also will print tree tags for each '(' character
        else:
            ans = self.data # print standardized syntax
        if len(self.children) > 0:
            for i in range(len(self.children)):
                if i == len(self.children)-1:
                    ans += str(self.children[i])
                else:
                    ans += str(self.children[i]) + ' '
            ans += ')'
        return ans
        
#errLog is a list of strings of error msgs that will be passed at each step of the tree-building process
def preProcess(inputString:str, errLog:List[str]=None, debug=False) -> list: #None will generate a warning since it's not a list of strings
    if errLog == None: #values assigned at func def, not each call, so need None vs []
        errLog = []
    #orig=inputString #saving original to refer to later, but might not be needed
    # inputString = inputString.lower()  #decided to permit uppercase letters and make it case sensitive to allow M vs m. caution: now  "If" is not "if"inputString=inputString.replace("]",")").replace("[","(").replace("{","(").replace("}",")").replace("\t"," ").replace("\r"," ").replace("\n"," ").replace("("," ( ").replace(")"," ) ")
    inputString = " ".join(inputString.split()) #this will remove consecutive spaces and also strip whitespace from front&back
    if inputString == "": #needed to avoid an issue in checking first character as (
        errLog.append("no input detected")
        return [], errLog
    # note that final replacement at end of next line attaches a \s to parens for list-splitting purposes
    
    parenPairing = 0
    for ind in range(len(inputString)): # needed to loop over index values rather than char to know if not at end
        char = inputString[ind]
        if char not in AllowedChars:
            errLog.append(f"{char} not an allowed character")
        if char == '(':
            parenPairing += 1
        elif char == ')':
            parenPairing -= 1
        # the following conditionals refer to the general lists of chars in case later developers decide not to the the replacements
        if char in openGroupSymb and parenPairing==1 and 0<ind<len(inputString)-1:  #i.e. parens balanced in the interior of the string
            errLog.append("contains multiple independent subexpressions") #"(stuff)(stuff)".  need )( check to insure "34" doesn't trigger err
        if char in whitespace and inputString[0] not in openGroupSymb:
            errLog.append("multiple elements should be contained within a list")
    if parenPairing < 0:
        errLog.append("too many )")
    elif parenPairing > 0:
        errLog.append("too many (")
    #else:  #I don't think this is needed anymore
    #    inputString = re.sub(r'\s+', ' ', inputString).replace("(", " ( ").replace(")", " ) ").split(' ')
    #    inputString = [element for element in inputString if element != ''] 
    return inputString.split(),errLog
    
def findMatchingParenthesis(tokenList, index):
    count = 1
    for i in range(index+1, len(tokenList)):
        if tokenList[i] == '(':
            count += 1
        elif tokenList[i] == ')':
            count -= 1     
        if count == 0:
            return i

def buildTree(inputList:list[str], errLog, debug=False) -> list:
    # if inputList == [], return the empty list
    if len(inputList) == 0:
        return [] 
    
    # we have something in inputList, create a Node
    node = Node([], debug=debug) # need [] inside Node init to ensure empty children list when created
    node.data = inputList[0]

    # if the first token is not '(', it is a single literal
    if inputList[0] != '(':

        # create Node where Node.data is the literal and continue processing the rest of input
        return [node] + buildTree(inputList[1:len(inputList)], debug)
     
    if inputList[0] == '(' and inputList[1] == ')':
        
        # special case for the empty list '()', just modify Node.data == '()'
        node.data = 'null'

        # continue processing the rest of input
        return [node] + buildTree(inputList[2:len(inputList)], debug)
    
    # we have '(' as the first token, find the index of its matching ')'
    matchIndex = findMatchingParenthesis(inputList,0)

    # if everything else is contained within our parenthesis pair, they will be contained in Node.children
    if matchIndex + 1 == len(inputList):
        node.children = buildTree(inputList[1:-1], debug)
        return [node]
    
    # there are multiple elements in our list, create a Node/subtree for things in that list, append all to Node.children
    node.children += buildTree(inputList[1:matchIndex], debug)

    # continue processing the rest of input
    return [node] + buildTree(inputList[matchIndex+1:len(inputList)], debug)