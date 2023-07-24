from flask import Blueprint, request
from flask_login import current_user

from exts import db
from models import OAuth, Task

bp = Blueprint("task", __name__)


# Validate access token in the request header
def validate_access_token(request):
    token = request.headers.get("Authorization")
    if token:
        access_token = token.split()[1]

        oauth = OAuth.query.filter(
            OAuth.token.like('%"access_token": "%{}%"%'.format(access_token))
        ).first()

        if not oauth:
            raise Exception("Access denied: Invalid access token.")
        return oauth
    else:
        raise Exception("Access denied: Invalid access token.")


# Get existing task item(s) from database
## IF task_id is provided, get the specific task item
## ELSE return all task items
def get_tasks(task_id=None):
    if current_user.is_authenticated:
        if task_id:
            return Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        return current_user.task
    else:
        oauth = validate_access_token(request)
        user = oauth.user
        if task_id:
            return Task.query.filter_by(id=task_id, user_id=user.id).first()
        return user.task


# Create a new task items 
## IF user is logged in, link the new task to the user
## ELSE validate the access token before linking the new task to the user
def create_task(task_name):
    task = Task(task_name=task_name) 
    if current_user.is_authenticated:
        task.user = current_user
    else:
        oauth = validate_access_token(request)
        task.user = oauth.user
    return task


# REST API: Add a Todo item
@bp.route("/add/<task_name>", methods=["POST"])
def add_task(task_name):
    try:
        # Add the new item
        task = create_task(task_name)
        db.session.add(task)
        db.session.commit()
        return "TODO item is successfully added."
    except Exception as e:
        return f"Failed to add the TODO item - {str(e)}"


# REST API: Delete a Todo item
@bp.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        task = get_tasks(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return f"TODO item {task_id} is successfully deleted."
        else:
            raise Exception(f"Item {task_id} is not found in your records.")
    except Exception as e:
        return f"Failed to delete the TODO item - {str(e)}"


# REST API: List all Todo items
@bp.route("/list", methods=["GET"])
def list_task():
    try:
        tasks = get_tasks()
        if tasks:
            task_list = "List of TODO items:\n\n"
            for task in tasks:
                dict_task = task.__dict__
                task_list += "Task ID: {}\nTask name: {}\nCreated on: {}\nCompleted: {}\n\n".format(
                    dict_task['id'],
                    dict_task['task_name'],
                    dict_task['created_on'],
                    dict_task['completed']
                )
            return task_list
        else:
            raise Exception("No task found in your records.")
    except Exception as e:
        return f"Failed to list the TODO items - {str(e)}"


# # REST API: Mark a Todo item as complete
@bp.route("/mark-complete/<int:task_id>", methods=["PUT"])
def mark_task_complete(task_id):
    try:
        task = get_tasks(task_id)
        if task:
            task.completed = 1
            db.session.commit()
            return f"TODO item {task_id} is successfully marked as complete."
        else:
            raise Exception(f"Item {task_id} is not found in your records.")
    except Exception as e:
        return f"Failed to mark the TODO item as complete - {str(e)}"
