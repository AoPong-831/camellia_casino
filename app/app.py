from flask import Flask, render_template, request, redirect, url_for, session
from models.models import Chip_database#database読み込み
from models.database import db_session#inset処理用
from datetime import datetime#レコードのタイムスタンプ用
from app import key#ログイン用(session管理に使う)のシークレットキー
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = key.SECRET_KEY#シークレットキー

db_uri = "sqlite:///" + os.path.abspath(os.path.join(app.root_path, '../models', 'chip.db')) # 追加(自分で一部変更した{os.path.abspath})
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri # 追加
db = SQLAlchemy(app) # 追加

class Chip_database(db.Model): # 追加
    __tablename__ = "chip_database" # 追加
    id = db.Column(db.Integer, primary_key=True) # 追加
    name = db.Column(db.String(), nullable=False) # 追加
    birth = db.Column(db.String(), nullable=False) # 追加
    chip = db.Column(db.Integer, nullable=False) # 追加
    money = db.Column(db.Integer, nullable=False) # 追加
    date = db.Column(db.String(), nullable=False) # 追加

#topページ
@app.route("/")
@app.route("/index",methods=["get","post"])
def index():
    if "user_name" in session:#ログインしている場合
        name = session["user_name"]
        if name == "root":#rootの場合
            return redirect(url_for("root"))
        chip_list = Chip_database.query.all()#database読み込み
        return render_template("top.html",chip_list=chip_list)
    else:#ログインしていない場合
        return redirect(url_for("login"))

#rootページ
@app.route("/root",methods=["get","post"])
def root():
    if "user_name" in session:#ログインしている場合
        name = session["user_name"]
        if name == "root":#rootの場合
            
            chip_list = Chip_database.query.all()#database読み込み
            return render_template("root.html",chip_list=chip_list)
        else:#rootでない場合
            return redirect(url_for("index"))
    else:#ログインしていない場合
        return redirect(url_for("login"))


#ログイン処理・ログインページ
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

#ログアウト処理
@app.route("/logout",methods=["post"])
def logout():
    session.pop("user_name", None)
    return redirect(url_for("login"))#ログインページにリダイレクト

#Create(試作)
@app.route("/add",methods=["post"])
def add():
    chip_db = Chip_database()#dbのインスタンスを作る(sqlalchemy)
    chip_db.name = request.form["name"]
    chip_db.birth = request.form["birth"]
    chip_db.chip = 0
    chip_db.money = 0
    db.session.add(chip_db)#以下terminalと同様の処理
    db.session.commit()
    return redirect(url_for("index"))

#Update(rootのみ)
@app.route("/update",methods=["post"])
def update():
    content = Chip_database.query.filter_by(name=request.form.get("name")).first()#id=request.form.get("update") >> name=request.form.get("name")に変更したら行けた。nameはquniqueだから良いのでは？？
    if content:#該当レコードがある場合
        content.name = request.form["name"]
        content.birth = request.form["birth"]
        db.session.commit()
    return root()

#Delete(rootのみ)
@app.route("/delete",methods=["post"])
def delete():
    id_list = request.form.getlist("delete")
    for id in id_list:
        content = Chip_database.query.filter_by(id=id).first()
        if content:#該当レコードがあれば
            db.session.delete(content)
    db.session.commit()
    return root()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)