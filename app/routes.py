from flask import request, render_template
from app import app, db
from app.models import Task



@app.route("/")
def display_homepage():
    return render_template("index.html")


@app.route('/tasks')
def get_tasks():
    search = request.args.get('q')
    sel_stmt = db.select(Task)
    if search:
        sel_stmt = sel_stmt.where(Task.title.ilike('%'+ search +'%'))
    tasks = db.session.execute(sel_stmt).scalars().all()
    return [t.to_dict() for t in tasks]


@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    return {'error' : f'Unable to find task of id: {task_id}'}, 404


@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.is_json:
        return {'error' : 'Content not a JSON'}, 400
    
    data = request.json
    # check to make sure the data is valid
    required_keys = ["title", "description"]
    missing_keys = []
    for key in required_keys:
        if key not in data:
            missing_keys.append(key)
    if missing_keys:
        return {"error" : f"Keys: {', '.join(missing_keys)} are missing from request"}, 400
    
    title = data.get('title')
    description = data.get('description')
    completed = data.get('completed', False)

    new_task = Task(title, description, completed)

    return new_task.to_dict(),201