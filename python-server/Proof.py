from ExpressionList import ExpressionList
# from Rule import Rule
# from RuleList import RuleName
from ProofLine import ProofLine
from Expression import Expression
from RuleList import RuleList
from TList import TList
from GUID import GUID

class Proof:
    def __init__(self):
        self.premises : TList(Expression) = None
        self.conclusion : Expression = None
        self.allowed_rules : RuleList = None
        self.content : TList(ProofLine) = None
        self.isValid = False
        self.isComplete = False
        self.title = ''
        self.id = GUID('proof')
    
    def setRules(self, rule_list:RuleList):
        if isinstance(rule_list,RuleList):
            self.allowed_rules = rule_list
        else:
            print('Error')

    def addLine(self, proofLine:ProofLine):
        if isinstance(proofLine, ProofLine):
            self.content += proofLine
        else:
            print('Error')

    def checkValidity(self):
        pass

    def checkComplete(self):
        return self.checkValidity() & self.checkPremises() & self.checkConclusion()

    def checkPremises(self):
        pass

    def checkConclusion(self):
        return self.conclusion == self.content[-1].argument

    def setConclusion(self, conclusion:Expression):
        if isinstance(conclusion, Expression):
            self.conclusion = conclusion
        else:
            print('Error')
    
    def setPremises(self, premises:TList[Expression]):
        if isinstance(premises,TList) and premises.T==Expression:
            self.premises = premises
        else:
            print('Error')

    # For testing the iterative structure of subproofs
    def print(self):
        print(f'{self}')

    def __str__(self):
        s = ''
        for line in self.content:
            s += f'{line}'
        return s