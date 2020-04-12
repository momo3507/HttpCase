# coding: utf-8
import uuid
from flask import Flask, request,jsonify
import time
import random

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    return jsonify({"ret": 0, "user": username, "pwd": password, "msg": "成功","token":str(uuid.uuid4())})

@app.route("/query",methods=["GET"])
def query():
    return jsonify({"ret":0})


if __name__ == '__main__':
    app.run()
