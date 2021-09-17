from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    task = db.Column(db.String(250), nullable=False)
    complete = db.Column(db.Boolean)


db.create_all()


@app.route("/")
def home():
    today = date.today()
    current_year = today.year
    return render_template("index.html", year=current_year)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_todo = Todo(
            task=request.form["task"],
            complete=False
        )
        db.session.add(new_todo)
        db.session.commit()
    todo_list = Todo.query.all()
    # print(todo_list)
    return render_template("add.html", todo_list=todo_list)


@app.route("/delete")
def delete():
    task_id = request.args.get("id")
    task_to_delete = Todo.query.get(task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for("add"))


@app.route("/done/<int:todo_id>")
def done(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("add"))


if __name__ == "__main__":
    app.run(debug=True)
