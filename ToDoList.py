import myDatabase
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId



app = Flask(__name__)
#gotta restrict CORS to local Vite dev server
CORS(app, resources={r"/*": {"origins": "http://localhost:\d+"}})


connect = myDatabase.Database(os.environ["mongodbKey"])
if "Notes" not in connect.client.list_database_names():
    connect.db = connect.client["Notes"]
else:
    connect.openDatabase("Notes")


#decorator, gives flask a way to map a URL path to a function in python
#when visiting this URL, the function is called
@app.route("/rename-collection/<newName>", methods=["PUT"])
def renameCollection(newName):
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    if not newName:
        return jsonify({"message": "newName is required"}), 400
    if connect.collection.name != newName:
        if not connect.renameCheck():
            return jsonify({"message" : "No connection to databse"})

    return jsonify({"message":"returning"})

@app.route("/delete-collection", methods=["DELETE"])
def deleteCollection():
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    
    if not connect.moveCollectionToTrash(connect.collection.name):
        return jsonify({"message" : "No connection to databse"})
    
    return jsonify({"message" : "returning"})

@app.route("/add-collection", methods=["POST"])
def createCollection():
    if connect.db is None:
        return jsonify({"message": "database not open"}), 400
    col = []
    if not connect.createCollection("New Category"):
        return jsonify({"message" : "No connection to databse"})
    else:
        col = connect.db.list_collection_names()
    return jsonify(col)

@app.route("/add-item-blank", methods=["POST"])
def insertBlankData():
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    if not connect.insertData({"title": "New Item", "body" : " "}):
        return jsonify({"message" : "No connection to databse"})
    return jsonify({"message":"returning"})

@app.route("/all-items", methods=["GET"])
def getAllItems():
    if connect.collection is None:
        return jsonify([])
    if not connect.testConnection():
        return jsonify([])

    
    return jsonify(connect.getAllItems(connect.collection))

@app.route("/all-collections", methods=["GET"])
def getAllCollectionNames():
    if not connect.testConnection():
        return jsonify([])

    if connect.db is None:
        connect.openDatabase("Notes")
  
    col = connect.db.list_collection_names()
    return jsonify(col)

@app.route("/collection-name", methods=["GET"])
def getCollectionName():
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400


    return jsonify({"collection_name": connect.collection.name})

@app.route("/set-collection", methods=["POST"])
def setCollection():
    if not connect.testConnection():
        return jsonify([])
    data = request.get_json()
    connect.openCollection(data.get('colName'))
    if connect.collection is None:
        return jsonify([])
    return jsonify(connect.getAllItems(connect.collection))

@app.route("/edit-itemTitle/<itemID>", methods=["PUT"])
def updateItemTitle(itemID):

    title = request.json.get("content", "")
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    try:
        conv = ObjectId(itemID)
    except:
        return jsonify({"message": "invalid id"}), 400
    if not connect.updateTitle(conv, title):
        return jsonify({"message" : "No connection to databse"})
    return jsonify({"message": "returning"})

@app.route("/edit-itemBody/<itemID>", methods=["PUT"])
def updateItemBody(itemID):
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    try:
        conv = ObjectId(itemID)
    except:
        return jsonify({"message": "invalid id"}), 400
    body = request.json.get("content","")
    
    if not connect.updateBody(conv, body):
        return jsonify({"message" : "No connection to databse"})
    return jsonify({"message": "returning"})

@app.route("/delete-item/<itemID>", methods=["DELETE"])
def deleteItem(itemID):
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    try:
        conv = ObjectId(itemID)
    except:
        return jsonify({"message": "invalid id"}), 400
    if not connect.moveItemToTrash({"_id": conv}):
        return jsonify({"message" : "No connection to databse"})
    return jsonify({"message" : "all good"})
    



# TRASH
@app.route("/trash/get-all-elements", methods=["GET"])
def getAllElements():
    data = []
    for name in connect.trash.list_collection_names():
        if name != "trash items":
            data.append({"type": "collection", "title": name})
    allItems = connect.getAllItems(connect.trashCollection)
    for item in allItems:
        data.append(item)

    return jsonify(data)

@app.route("/trash/delete-element/<identifier>/<elementType>", methods=["DELETE"])
def deleteElement(identifier, elementType):
    if elementType == "collection":
        connect.deleteTrashCollection(identifier)
    elif elementType == "item":      
        try:       
            conv = ObjectId(identifier)
        except:
            return jsonify({"message": "invalid id"}), 400
        connect.deleteTrashItem({"_id":conv})

    return jsonify({"message" : "deleted"})

@app.route("/trash/restore-element/<identifier>/<elementType>/<destination>", methods=["PUT"])
def restoreElement(identifier, elementType, destination):
    

    if elementType == "item":
        if destination in connect.db.list_collection_names():
            try:       
                conv = ObjectId(identifier)
            except:
                return jsonify({"message": "invalid id"}), 400
            connect.db[destination].insert_one(connect.trashCollection.find_one({"_id":conv}))
            connect.deleteTrashItem({"_id":conv})
    elif elementType == "collection":
        connect.restoreCollection(identifier)


    return jsonify({"message" : "restored"})

@app.route("/trash/delete-all-items", methods=["DELETE"])
def deleteAllItems():
    if not connect.deleteAllTrashItems():
        return jsonify({"message" : "No connection to databse"})
    return jsonify({"message" : "deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)