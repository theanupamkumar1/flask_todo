from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    number = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.number}-{self.title}"


@app.route("/", methods=["GET", "POST"])
def welcome():
    if request.method == "POST":
        # just for oue sake to check post is working, "post" will be printed on console
        print("post")
        print(request.form["title"])
        t = request.form["title"]
        d = request.form["desc"]
        todo_obj = Todo(title=t, desc=d)
        db.session.add(todo_obj)
        db.session.commit()

    # todo_obj = Todo(title="2st to do", desc="write here")
    # db.session.add(todo_obj)
    # db.session.commit()

    all_todos = Todo.query.all()
    print(all_todos)

    return render_template("home.html", my_todos=all_todos)


@app.route("/delete/<int:number>")
def delete(number):
    print(number)
    all_todos = Todo.query.filter_by(number=number).first()
    db.session.delete(all_todos)
    db.session.commit()
    print(f"todo {number} is deleted")
    return redirect("/")
    # all_todos = Todo.query.all()
    # return render_template("home.html", my_todos=all_todos)


@app.route("/update/<int:number>", methods=["POST", "GET"])
def update(number):
    if request.method == "POST":
        t = request.form["title"]
        d = request.form["desc"]
        selected_todos = Todo.query.filter_by(number=number).first()
        selected_todos.title = t
        selected_todos.desc = d
        db.session.add(selected_todos)
        db.session.commit()
        return redirect("/")

    all_todos = Todo.query.filter_by(number=number).first()
    return render_template("update.html", todo=all_todos)


@app.route("/base")
def base():
    return render_template("base.html")


@app.route("/show")
def alltodos():
    all_todos = Todo.query.all()
    print(all_todos)


@app.route("/model", methods=["GET"])
def model():
    return "<pre>this is model page <h1>nigga</h1> </pre>"


## Variable rule
@app.route("/success/<int:score>")
def success(score):
    return "The person has passed and the score is:" + str(score)


@app.route("/fail/<int:score>")
def fail(score):
    return "The person has failed"


@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
    else:
        math = int(request.form["maths"])
        science = int(request.form["science"])
        history = int(request.form["history"])
        avg = (math + science + history) / 3

        result = ""
        if avg >= 75:
            result = "success"
        else:
            result = "fail"

        return redirect(url_for(result, score=avg))


@app.route("/api", methods=["POST"])
def calulate_sum():
    data = request.get_json()
    a_val = int(dict(data)["a"])
    b_val = int(dict(data)["b"])

    return jsonify(a_val + b_val)
    # return render_template("form.html", score=avg)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
