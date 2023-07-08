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


# REST API: Add a Todo item
@bp.route("/add/<task_name>", methods=["POST"])
def add_task(task_name):
    try:
        # IF user is logged in, create a new task item
        # ELSE validate the access token before creating a new task item
        if current_user.is_authenticated:
            task = Task(task_name=task_name)
            task.user = current_user
        else:
            oauth = validate_access_token(request)
            task = Task(task_name=task_name) 
            task.user = oauth.user

        # Add the new item
        db.session.add(task)
        db.session.commit()
        return "TODO item is successfully added."
    except Exception as e:
        return f"Failed to add the TODO item - {str(e)}"


# REST API: Delete a Todo item
@bp.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        # IF user is logged in, query the task item
        # ELSE validate the access token before querying the task item
        if current_user.is_authenticated:
            task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        else:
            oauth = validate_access_token(request)
            task = Task.query.filter_by(id=task_id, user_id=oauth.user_id).first()

        # Delete the item found
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
        # IF user is logged in, query the task items
        # ELSE validate the access token before querying the task items
        if current_user.is_authenticated:
            tasks = Task.query.filter_by(user_id=current_user.id).all()
        else:
            oauth = validate_access_token(request)
            tasks = Task.query.filter_by(user_id=oauth.user_id).all()

        # Display the items
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
        # IF user is logged in, query the task item
        # ELSE validate the access token before querying the task item
        if current_user.is_authenticated:
            task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        else:
            # If user is not logged in, but an access token is provided
            oauth = validate_access_token(request)
            task = Task.query.filter_by(id=task_id, user_id=oauth.user_id).first()
        
        # Mark the task as complete
        if task:
            task.completed = 1
            db.session.commit()
            return f"TODO item {task_id} is successfully marked as complete."
        else:
            raise Exception(f"Item {task_id} is not found in your records.")
    except Exception as e:
        return f"Failed to mark the TODO item as complete - {str(e)}"

