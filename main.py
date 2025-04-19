from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

import sqlite3

def adduser(username: str, password: str):
    db = sqlite3.connect("usernames.db")
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS userbase (username VARCHAR(255), password VARCHAR(255))")
    cur.execute("SELECT * FROM userbase WHERE username = ?", (username))
    result = cur.fetchall()
    if len(result) == 0:
        cur.execute("INSERT INTO userbase (username, password) VALUES (?, ?)", (username, password))
        db.commit()
    db.close()


@app.route('/')
def main():
    return render_template("main.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/get")
def getUser():
    u = request.args.get("u")
    p = request.args.get("p")
    db = sqlite3.connect("usernames.db")
    cur = db.cursor()
    cur.execute("SELECT password FROM userbase WHERE username = ?", (u,))
    result = cur.fetchall()
    db.close()
    if len(result) == 1:
        stored_pw = result[0][0]
        if p == stored_pw:
            return "login successful. not sure what else to put here"
        else:
            return "wrong password"
    else:
        return f"{u} does not exist"


@app.route('/create')
def create():
    u = request.args.get("u")
    p = request.args.get('p')
    adduser(u,p)
    return "user added successfully or overlap with another user "+u+" <a href='/login'>go to login</a>"

if __name__ == '__main__':
    app.run(debug=True)