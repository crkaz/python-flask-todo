from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return "<Task %r>" % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        taskContent = request.form["content"]
        newTask = Todo(content=taskContent)
        try:
            db.session.add(newTask)
            db.session.commit()
            return redirect("/")
        except:
            return "Unexpected error."
    else:
        tasks = Todo.query.order_by(Todo.dateCreated).all()
        return render_template("index.html", tasks=tasks)


@app.route("/delete/<int:id>", methods=["GET"])
def delete(id):
    taskToDelete = Todo.query.get_or_404(id)
    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return redirect("/")
    except:
        return "Failed to delete"


@app.route("/update/<int:id>", methods=["GET", 'POST'])
def update(id):
    taskToUpdate = Todo.query.get_or_404(id)

    if request.method == 'POST':
        taskToUpdate.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Failed to update record.'
    else:
        return render_template('update.html', task=taskToUpdate)

if __name__ == "__main__":
    app.run(debug=True)
