from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi




class Database:
    
    client = None
    collection = None
    db = None
    trash = None
    trashCollection = None

    iterator = 0

    def __init__(self, uri):
        self.client = MongoClient(uri, server_api=ServerApi('1'));
        self.trash = self.client["Trash"]
        self.trashCollection = self.trash["trash items"]



    def openDatabase(self, name):
        if self.testConnection:
            if name in self.client.list_database_names():
                self.db = self.client[name]
                

    def openCollection(self, colName):
        if self.testConnection:
            if colName in self.db.list_collection_names():
                self.collection = self.db[colName]

    def createDatabase(self, name):
        if self.testConnection:
            if name not in self.client.list_database_names():
                self.db = self.client[name]

    def createCollection(self, colName):
        if self.testConnection:
            if colName not in self.db.list_collection_names():
                self.db.create_collection(colName);
                self.collection = self.db[colName]

    def createCollectionWithData(self, colName, title, body):
        if self.testConnection:
            if colName not in self.db.list_collection_names():
                self.collection = self.db[colName]
                data = {"title": title, "body": body}
                result = self.collection.insert_one(data)
    
    def updateTitle(self, _id, newTitle):
        if self.testConnection:
            if self.collection is not None:
                self.collection.update_one(
                        {"_id": _id},
                        {"$set": {"title": newTitle}}
                    )
    def updateBody(self, _id, body):
        if self.testConnection:
            if self.collection is not None:
                self.collection.update_one(
                        {"_id": _id},
                        {"$set": {"body": body}}
                    )
    def serialize(self, data):
        data["_id"] = str(data["_id"])
        return data

    def getAllItems(self):
        return [self.serialize(data) for data in self.collection.find()]

    def insertData(self, data):
        if self.testConnection:
            if self.collection is not None:
               
                #data = {"title": title, "body": body}
                result = self.collection.insert_one(data)

    def editCollectionName(self, colName, newName):
        if self.testConnection:
            if colName in self.db.list_collection_names():
                self.db[colName].rename(newName)
                
    

    def deleteDatabase(self, name):
        if self.testConnection:
            if name in self.client.list_database_names():
                self.client.drop_database(name)
                self.db = None

    def deleteCollection(self, colName):
        if self.testConnection:
            if colName in self.db.list_collection_names():
                self.db[colName].drop()

    def moveCollectionToTrash(self, colName):
        if self.testConnection:
            if colName in self.db.list_collection_names():
                newCol = colName
                if colName not in self.trash.list_collection_names():
                    self.trash.create_collection(newCol)
                else:
                    newCol = colName + str(self.iterator)
                    while newCol in self.trash.list_collection_names():
                        self.iterator += 1
                        newCol = colName + str(self.iterator)
                    self.trash.create_collection(newCol)
                for doc in self.db[colName].find({}):
                    self.trash[newCol].insert_one(doc)
                self.db[colName].drop()

                    

    def moveItemToTrash(self, _id):
        if self.testConnection:
            if self.collection is not None:
                move = self.collection.find_one(_id)
                self.trashCollection.insert_one(move)
                self.collection.delete_one(_id)
            else:
                print("Collection is None")
                

    def getCollection(self):
        return self.collection

    def getDatabase(self):
        return self.db

    def testConnection(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            return False



