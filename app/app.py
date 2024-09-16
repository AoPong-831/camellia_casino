from flask import Flask, render_template, request, redirect, url_for
from models.models import Chip_database#database読み込み
from models.database import db_session#inset処理用
from datetime import datetime#レコードのタイムスタンプ用


app = Flask(__name__)

@app.route("/")
@app.route("/index",methods=["get","post"])
def index():
    if request.method == "post":
        id = request.form.get("id")#idを受け取る
        if id == "aaa":#aaaだったらログイン成功
            return render_template("top2.html")
    
    chip_list = Chip_database.query.all()#database読み込み
    return render_template("top.html",chip_list=chip_list)

@app.route("/add",methods=["post"])
def add():
    name = request.form["name"]
    birth = int(request.form["birth"])
    chip = 0
    money = 0
    content = Chip_database(name,birth,chip,money,datetime.now())#追加するレコード作成
    db_session.add(content)#以下terminalと同様の処理
    db_session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)