from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import re


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
        if self.testConnection():
            if name in self.client.list_database_names():
                self.db = self.client[name]    
            return True
        else:
            return False
                

    def openCollection(self, colName):
        if self.testConnection():
            if colName in self.db.list_collection_names():
                self.collection = self.db[colName]
            return True
        else:
            return False

    def createDatabase(self, name):
        if self.testConnection():
            if name not in self.client.list_database_names():
                self.db = self.client[name]
            return True
        else:
            return False

    def createCollection(self, colName):
        if self.testConnection():
            if colName not in self.db.list_collection_names():
                self.db.create_collection(colName);
                self.collection = self.db[colName]
                self.collection.create_index([("flat", "text")])
            return True
        else:
            return False

    def setSearchIndices(self):
        if self.testConnection():
            for collection in self.db.list_collection_names():
                indices = self.db[collection].list_indexes()
                count = 0
                for i in indices:
                    count+=1
                if count == 1:
                    self.db[collection].create_index([("flat", "text")])
            return True
        else:
            return False

    def createCollectionWithData(self, colName, title, body):
        if self.testConnection():
            if colName not in self.db.list_collection_names():
                self.collection = self.db[colName]
                data = {"title": title, "body": body}
                result = self.collection.insert_one(data)
            return True
        else:
            return False
    
    def updateTitle(self, _id, newTitle):
        if self.testConnection():
            if self.collection is not None:
                self.collection.update_one(
                        {"_id": _id},
                        {"$set": {"title": newTitle}}
                    )
            return True
        else:
            return False

    def updateBody(self, _id, body, flat, collection):
        if self.testConnection():
            if collection in self.db.list_collection_names():
                self.db[collection].update_one(
                        {"_id": _id},
                        {"$set": {"body": body, "flat": flat}}
                    )
            return True
        else:
            return False

    def serialize(self, data):
        data["_id"] = str(data["_id"])
        return data

    def getAllItems(self, collection):
        return [self.serialize(data) for data in collection.find()]

    def insertData(self, data):
        if self.testConnection():
            if self.collection is not None:
                result = self.collection.insert_one(data)
            return True
        else:
            return False

    def editCollectionName(self, colName, newName):
        if self.testConnection():
            if colName in self.db.list_collection_names():
                self.db[colName].rename(newName)
            return True
        else:
            return False
                
    

    def deleteDatabase(self, name):
        if self.testConnection():
            if name in self.client.list_database_names():
                self.client.drop_database(name)
                self.db = None
            return True
        else:
            return False

    def deleteCollection(self, colName):
        if self.testConnection():
            if colName in self.db.list_collection_names():
                self.db[colName].drop()
            return True
        else:
            return False

    def moveCollectionToTrash(self, colName):
        if self.testConnection():
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
            return True
        else:
            return False

    def renameCheck(self, colName):
        if self.testConnection():
            self.collection.rename(colName)
            return True
        else:
            return False

    def moveItemToTrash(self, _id):
        if self.testConnection():
            if self.collection is not None:
                move = self.collection.find_one(_id)
                move["collection"] = self.collection.name
                self.trashCollection.insert_one(move)
                self.collection.delete_one(_id)
            else:
                print("Collection is None")
            return True
        else:
            return False
                
    def getSearchResults(self, text):
        if self.testConnection():
            pattern = re.compile(text, re.IGNORECASE)
            query = {"flat": {"$regex": pattern}}
            #query = {"$text" : {"$search": text}}
            results = []
            for collection in self.db.list_collection_names():
                for doc in self.db[collection].find(query):
                    doc["collection"] = collection
                    results.append(doc)
            return [self.serialize(data) for data in results]
        else:
            return False

    def getCollection(self):
        return self.collection

    def getDatabase(self):
        return self.db


    # TRASH
    def deleteAllTrashItems(self):
        if self.testConnection():
            for doc in self.trashCollection.find():
                self.trashCollection.delete_one(doc)
            return True
        else:
            return False
    def deleteTrashCollection(self,colName):
        if self.testConnection():
            if colName in self.trash.list_collection_names():
                self.trash.drop_collection(colName)
            return True
        else:
            return False

    def deleteTrashItem(self,_id):
        if self.testConnection():
            self.trashCollection.delete_one(_id)
            return True
        else:
            return False

    def restoreCollection(self, colName):
        if self.testConnection():
            newCol = colName
            if newCol not in self.db.list_collection_names():
                self.db.create_collection(newCol)
                self.db[newCol].create_index([("flat", "text")])
            else:
                newCol = colName + str(self.iterator)
                while newCol in self.db.list_collection_names():
                    self.iterator += 1
                    newCol = colName + str(self.iterator)
                self.db.create_collection(newCol)
                self.db[newCol].create_index([("flat", "text")])
            for doc in self.trash[colName].find({}):
                self.db[newCol].insert_one(doc)
            self.trash[colName].drop()
            return True
        else:
            return False

    def testConnection(self):
        try:
            self.client.admin.command('ping')
            return True
        except Exception as e:
            return False



