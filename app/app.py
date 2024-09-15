from flask import Flask, render_template, request
#database読み込み
from models.models import Chip_database

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        id = request.form.get("id")#idを受け取る
        if id == "aaa":#aaaだったらログイン成功
            return render_template("top2.html")
    
    chip_list = Chip_database.query.all()#database読み込み
    return render_template("top.html",chip_list=chip_list)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)