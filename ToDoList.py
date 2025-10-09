import myDatabase
import os
import socket
import subprocess
import threading
import time
import sys
import atexit
import signal
import webbrowser
import re
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from bson import ObjectId


frontendProcess = None



def getFreePort():
    s = socket.socket()
    s.bind(('',0))
    port = s.getsockname()[1]
    s.close()
    return port

def connectLocally():
    storeDir = os.path.join(os.getcwd(), "Data")
    mongoD = os.path.join(os.getcwd(), "MongoDB", "Server","8.2","bin", "mongod.exe")

    if not os.path.exists(storeDir):
        os.makedirs(storeDir)

    # need to find a free port
    port = getFreePort()

    process = subprocess.Popen([
        mongoD,
        "--dbpath", storeDir,
        "--bind_ip", "127.0.0.1",
        "--port", str(port),
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    return port


app = Flask(__name__)


def runFrontEnd():
    global frontendProcess
    enviro = os.environ.copy()
    enviro["NO_COLOR"] = '1'
    url = None

    frontendProcess = subprocess.Popen(
        ["npm", "run","dev", "--no-color"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        cwd="Frontend/frontend",
        shell=True,
        text=True,
        encoding="utf-8",
        env=enviro
        )
    for line in frontendProcess.stdout:
        print(line, end="")  # optional: log Vite output
        match = re.search(r"Local:\s*(http://localhost:(\d+))", line)
        if match:
            url = match.group(1)
            break
    webbrowser.open(url)

def stopFrontEnd():
    global frontendProcess
    if frontendProcess:
        if sys.platform.startswith("win"):
            frontendProcess.terminate()
        else:
            os.kill(frontendProcess.pid, signal.SIGTERM)
        frontendProcess.wait()

atexit.register(stopFrontEnd)

#gotta restrict CORS to local Vite dev server
CORS(app, resources={r"/*": {"origins": r"http://localhost:\d+"}})
threading.Thread(target=runFrontEnd, daemon=True).start()



#LOCAL
port = connectLocally()
connect = myDatabase.Database(f"mongodb://localhost:{port}/")


# CLOUD
#connect = myDatabase.Database(os.environ["mongodbKey"])


if "Notes" not in connect.client.list_database_names():
    connect.db = connect.client["Notes"]
else:
    connect.openDatabase("Notes")

if len(connect.db.list_collection_names()) < 1:
    connect.createCollection("New Category")

# connect.setSearchIndices()







# when visiting this URL, the function is called
@app.route("/rename-collection/<newName>", methods=["PUT"])
def renameCollection(newName):
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    if not newName:
        return jsonify({"message": "newName is required"}), 400
    if connect.collection.name != newName:
        if not connect.renameCheck(newName):
            return jsonify({"message" : "No connection to database"})

    return jsonify({"message":"returning"})

@app.route("/delete-collection", methods=["DELETE"])
def deleteCollection():
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    
    if not connect.moveCollectionToTrash(connect.collection.name):
        return jsonify({"message" : "No connection to database"})
    
    return jsonify({"message" : "returning"})

@app.route("/add-collection", methods=["POST"])
def createCollection():
    if connect.db is None:
        return jsonify({"message": "database not open"}), 400
    col = []
    if not connect.createCollection("New Category"):
        return jsonify({"message" : "No connection to database"})
    else:
        col = connect.db.list_collection_names()
    return jsonify(col)

@app.route("/add-item-blank", methods=["POST"])
def insertBlankData():
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    if not connect.insertData({"title": "New Item", "body" : " "}):
        return jsonify({"message" : "No connection to database"})
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
    if not itemID:
        return jsonify({"message": "Invalid ID"})

    title = request.json.get("content", "")
    if connect.collection is None:
        return jsonify({"message": "no active collection"}), 400
    try:
        conv = ObjectId(itemID)
    except:
        return jsonify({"message": "invalid id"}), 400
    if not connect.updateTitle(conv, title):
        return jsonify({"message" : "No connection to database"})
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
    flat = request.json.get("flat", "")
    collection = request.json.get("destination")
    
    if not connect.updateBody(conv, body, flat, collection):
        return jsonify({"message" : "No connection to database"})
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
        return jsonify({"message" : "No connection to database"})
    return jsonify({"message" : "all good"})
    

# SEARCH
@app.route("/search/query-all-collections/<text>", methods=["GET"])
def getResults(text):
    return jsonify(connect.getSearchResults(text))


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
        else:
            return jsonify({"message" : "Destination collection doesn't exist"})
    elif elementType == "collection":
        if not connect.restoreCollection(identifier):
            return jsonify({"message" : "No connection to database"})


    return jsonify({"message" : "restored"})

@app.route("/trash/delete-all-items", methods=["DELETE"])
def deleteAllItems():
    if not connect.deleteAllTrashItems():
        return jsonify({"message" : "No connection to database"})
    return jsonify({"message" : "deleted"})


if __name__ == "__main__":
    from waitress import serve
    import logging

    logging.getLogger('waitress.queue').setLevel(logging.ERROR)


    serve(app, port=5000)
    
    