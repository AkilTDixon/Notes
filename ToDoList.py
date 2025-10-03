import myDatabase
import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)
CORS(app)


connect = myDatabase.Database(os.environ["mongodbKey"])
connect.openDatabase("Notes")


#decorator, gives flask a way to map a URL path to a function in python
#when visiting this URL, the function is called
@app.route("/rename-collection/<newName>", methods=["PUT"])
def renameCollection(newName):
    if connect.collection.name != newName:
        connect.collection.rename(newName)
    return jsonify({"message":"returning"})

@app.route("/delete-collection", methods=["DELETE"])
def deleteCollection():
    connect.moveCollectionToTrash(connect.collection.name)
    return jsonify({"message" : "returning"})

@app.route("/add-collection", methods=["POST"])
def createCollection():
    connect.createCollection("New Category")
    col = connect.db.list_collection_names()
    return jsonify(col)

@app.route("/add-item-blank", methods=["POST"])
def insertBlankData():
    connect.insertData({"title": "New Item", "body" : " "})
    return jsonify({"message":"returning"})

@app.route("/all-items", methods=["GET"])
def getAllItems():
    return jsonify(connect.getAllItems())

@app.route("/all-collections", methods=["GET"])
def getAllCollectionNames():
    col = connect.db.list_collection_names()
    return jsonify(col)

@app.route("/collection-name", methods=["GET"])
def getCollectionName():
    if connect.collection is not None:
        return jsonify({"collection_name": connect.collection.name})

@app.route("/set-collection", methods=["POST"])
def setCollection():
    data = request.get_json()
    connect.openCollection(data.get('colName'))
    return jsonify(connect.getAllItems())

@app.route("/edit-itemTitle/<itemID>", methods=["PUT"])
def updateItemTitle(itemID):
    title = request.json.get("content", "")
    connect.updateTitle(ObjectId(itemID), title)
    return jsonify({"message": "returning"})

@app.route("/edit-itemBody/<itemID>", methods=["PUT"])
def updateItemBody(itemID):
    body = request.json.get("content","")
    connect.updateBody(ObjectId(itemID), body)
    return jsonify({"message": "returning"})

@app.route("/delete-item/<itemID>", methods=["DELETE"])
def deleteItem(itemID):
    connect.moveItemToTrash({"_id": ObjectId(itemID)})
    return jsonify({"message" : "all good"})
    


if __name__ == "__main__":
    app.run(debug=True, port=5000)