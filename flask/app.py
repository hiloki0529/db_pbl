#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, session, redirect, jsonify
from datetime import timedelta, datetime
import re
from db import login

app = Flask(__name__)
app.secret_key = "AdfivjArifgalfgngav248dgFVifg:p4932hdvs"

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)
    if session.get("username") is not None:
        return
    elif request.path == "/login" or request.path == "/sign_up":
        return
    else:
        return redirect("/login")

@app.route("/")
def hello():
    return render_template("main.html")

@app.route("/hello", methods=["POST","GET"])
def hi():
    if request.method == "POST":
        name = request.form["name"]
        return render_template("main.html", name=name)

@app.route('/login', methods = ['GET', 'POST'])
def login_page():
    failed = ""
    if request.method == 'POST':
        if login(request.form)[0]:
            if login(request.form)[1]:
                session['username'] = request.form['username']
                session["wriong"] = 0
                return redirect('/')
            else:
                session["wrong"] += 1
        if session["wrong"] >= 3:
            failed = " FAILED!!!!!!"
        else:
            failed="failed"
    else:
        session["wrong"] = 0
    return render_template("login.html", failed=failed)

@app.route("/logout")
def logout():
	session.pop("username", None)
	return redirect("/")

@app.route("/sign_up", methods = ["GET", "POST"])
def signup():
    if request.method == "POST":
        return redirect("/")
    return render_template("signup.html")

@app.route("/deny", methods = ["GET"])
def deny():
    return render_template("deny.html")

if __name__=="__main__":
	app.run(host="0.0.0.0", port=8080)
