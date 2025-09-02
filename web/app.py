from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from pymongo import MongoClient
from bson import ObjectId
import json
import os

sample = Flask(__name__)

data = []
mongo_uri = os.environ.get("MONGO_URI")
db_name = os.environ.get("DB_NAME")

## ---- mongoDB ----
# connect to mongo
client = MongoClient(mongo_uri)
mydb = client[db_name]
mycol = mydb["routers"]
interface = mydb["interface_status"]

data = mycol.find()


@sample.route("/")
def main():
    data = mycol.find()
    return render_template("index.html", data=data)


@sample.route("/router/<router_ip>")
def show_route(router_ip):
    data = list(interface.find({"router_ip": router_ip}).sort("timestamp", -1).limit(3))
    return render_template("router.html", data=data)


@sample.route("/add", methods=["POST"])
def add_comment():
    ip = request.form.get("ip")
    username = request.form.get("username")
    password = request.form.get("password")

    if ip and username and password:
        info = {"ip": ip, "username": username, "password": password}
        res = mycol.insert_one(info)
    return redirect(url_for("main"))


@sample.route("/delete", methods=["POST"])
def delete_comment():
    try:
        idx = int(request.form.get("idx"))
        col = {"_id": data[idx]["_id"]}
        res = mycol.delete_one(col)
    except Exception:
        pass
    return redirect(url_for("main"))


if __name__ == "__main__":
    sample.run(host="0.0.0.0", port=5050)
