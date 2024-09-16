from flask import Flask, render_template, request, redirect, url_for, session
from models.models import Chip_database#database読み込み
from models.database import db_session#inset処理用
from datetime import datetime#レコードのタイムスタンプ用
from app import key#ログイン用(session管理に使う)のシークレットキー

app = Flask(__name__)
app.secret_key = key.SECRET_KEY#シークレットキー


@app.route("/")
@app.route("/index",methods=["get","post"])
def index():
    if "user_name" in session:#ログインしている場合
        name = session["user_name"]
        chip_list = Chip_database.query.all()#database読み込み
        return render_template("top.html",chip_list=chip_list)
    else:
        return redirect(url_for("login"))

#ログインページ
@app.route("/login",methods=["get","post"])
def login():
    if request.method == "POST":
        name = request.form["name"]#user_nameをwebの入力欄から取得
        user = Chip_database.query.filter_by(name=name).first()#databaseから該当ユーザのレコードを取得
        if user:#name一致
            birth = request.form["birth"]
            if user.birth == birth:#birth一致
                session["user_name"] = name
                return redirect(url_for("index"))
            else:
                return redirect(url_for("login",status="wrong_password"))
        else:#name不一致
            return redirect(url_for("login",status="user_notfound"))
    else:
        status = request.args.get("status")#エラーメッセージを受け取る
        if status == None:status = ""#status空白化
        return render_template("login.html",status=status)

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