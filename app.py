import os
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
database_url = os.environ.get("DATABASE_URL", "sqlite:///levelup.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    category = db.Column(db.String(50), default="Personal")
    scheduled_time = db.Column(db.String(20), default="")
    active_date = db.Column(db.String(10), nullable=False, default=lambda: date.today().isoformat())
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    if not Task.query.first():
        starter = [
            ("DSA practice", "DSA", "07:00", date.today().isoformat()),
            ("Data Science classes", "Data Science", "09:30", date.today().isoformat()),
            ("Practical / revision", "Practice", "14:00", date.today().isoformat()),
            ("Gym", "Fitness", "16:00", date.today().isoformat()),
            ("English practice", "English", "18:00", date.today().isoformat()),
            ("Online class", "Class", "19:00", date.today().isoformat()),
        ]
        for title, category, when, day in starter:
            db.session.add(Task(title=title, category=category, scheduled_time=when, active_date=day))
        db.session.commit()

def record_visit():
    visit = Visit.query.order_by(Visit.id.desc()).first()
    if visit is None:
        visit = Visit(last_seen=datetime.utcnow())
        db.session.add(visit)
    else:
        visit.last_seen = datetime.utcnow()
    db.session.commit()

@app.route("/")
def index():
    with app.app_context():
        record_visit()
        selected_day = request.args.get("day", date.today().isoformat())
        tasks = Task.query.filter_by(active_date=selected_day).order_by(Task.scheduled_time, Task.id).all()
        total = len(tasks)
        done = sum(1 for task in tasks if task.completed)
        percent = round(done * 100 / total) if total else 0
        all_days = db.session.query(Task.active_date).distinct().order_by(Task.active_date.desc()).all()
        last_visit = Visit.query.order_by(Visit.id.desc()).first()
        return render_template("index.html", tasks=tasks, selected_day=selected_day,
                               total=total, done=done, percent=percent,
                               all_days=[x[0] for x in all_days],
                               last_visit=last_visit.last_seen if last_visit else None)

@app.post("/tasks/add")
def add_task():
    title = request.form.get("title", "").strip()
    if title:
        db.session.add(Task(title=title,
                            category=request.form.get("category", "Personal"),
                            scheduled_time=request.form.get("scheduled_time", ""),
                            active_date=request.form.get("active_date") or date.today().isoformat()))
        db.session.commit()
    return redirect(url_for("index", day=request.form.get("active_date") or date.today().isoformat()))

@app.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    task = db.get_or_404(Task, task_id)
    task.completed = not task.completed
    db.session.commit()
    return redirect(url_for("index", day=task.active_date))

@app.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    task = db.get_or_404(Task, task_id)
    day = task.active_date
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index", day=day))

@app.post("/tasks/<int:task_id>/edit")
def edit_task(task_id):
    task = db.get_or_404(Task, task_id)
    title = request.form.get("title", "").strip()
    if title:
        task.title = title
        task.category = request.form.get("category", task.category)
        task.scheduled_time = request.form.get("scheduled_time", task.scheduled_time)
        db.session.commit()
    return redirect(url_for("index", day=task.active_date))

@app.get("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(debug=True)
