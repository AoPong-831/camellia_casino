from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        id = request.form.get("id")#idを受け取る
        if id == "aaa":#aaaだったらログイン成功
            return render_template("top2.html")
    return render_template("top.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)