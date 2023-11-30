import random

class GUID():
    def __init__(self, type:str='', guid:'GUID'=None):
        # For randomly generating GUIDs we should consider something more robust
        # for security than the random library (based on clock value)
        if guid!=None:
            self.value = guid.value
        else:
            self.value = random.randbytes(16)
        self.type = type