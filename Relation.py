class Relation:
    def __init__(self, source, database, target ):
        self.source = source
        self.database = database
        self.target = target

    def getSource(self):
        return  self.source
    
    def getDatabase(self):
        return  self.database

    def getTarget(self):
        return  self.target
