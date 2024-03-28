from . import db
from datetime import datetime

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    def __init__(self, title:str, description:str, completed:bool):
        self.title = title
        self.description = description
        self.completed = completed
        self.save()
    

    def __repr__(self) -> str:
        return f"<Task {self.id} | title='{self.title}' description='{self.description}'>"


    # When creating a new Task, it will be added to our database
    def save(self):
        db.session.add(self)
        db.session.commit()


    def to_dict(self):
        return {
            "id" : self.id,
            "title" : self.title,
            "description" : self.description,
            "completed" : self.completed,
            "createdAt" : self.created_at
        }