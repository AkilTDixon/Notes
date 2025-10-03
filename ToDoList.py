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
        connect.collection.rename(newName)
    return jsonify({"message":"returning"})

@app.route("/delete-collection", methods=["DELETE"])
def deleteCollection():
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    connect.moveCollectionToTrash(connect.collection.name)
    return jsonify({"message" : "returning"})

@app.route("/add-collection", methods=["POST"])
def createCollection():
    if connect.db is None:
        return jsonify({"message": "database not open"}), 400
    connect.createCollection("New Category")
    col = connect.db.list_collection_names()
    return jsonify(col)

@app.route("/add-item-blank", methods=["POST"])
def insertBlankData():
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    connect.insertData({"title": "New Item", "body" : " "})
    return jsonify({"message":"returning"})

@app.route("/all-items", methods=["GET"])
def getAllItems():
    if connect.collection is None:
        return jsonify([])
    return jsonify(connect.getAllItems())

@app.route("/all-collections", methods=["GET"])
def getAllCollectionNames():
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
    data = request.get_json()
    connect.openCollection(data.get('colName'))
    if connect.collection is None:
        return jsonify([])
    return jsonify(connect.getAllItems())

@app.route("/edit-itemTitle/<itemID>", methods=["PUT"])
def updateItemTitle(itemID):
    title = request.json.get("content", "")
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    try:
        conv = ObjectId(itemID)
    except:
        return jsonify({"message": "invalid id"}), 400
    connect.updateTitle(conv, title)
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
    
    connect.updateBody(conv, body)
    return jsonify({"message": "returning"})

@app.route("/delete-item/<itemID>", methods=["DELETE"])
def deleteItem(itemID):
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    try:
        conv = ObjectId(itemID)
    except:
        return jsonify({"message": "invalid id"}), 400
    connect.moveItemToTrash({"_id": conv})
    return jsonify({"message" : "all good"})
    


if __name__ == "__main__":
    app.run(debug=True, port=5000)