import json

class Lot():
    def __init__(self,lotId,lotStatus):
        self.Id=lotId
        self.Blocked= lotStatus

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
    def getId(self):
        return self.Id
    
    def getStatus(self):
        return self.Blocked
    
