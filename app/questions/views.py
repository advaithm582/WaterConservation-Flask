from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user

from app import db
from app.models import Question
from app.questions.forms import (
    EditQuestionForm, 
    AddQuestionForm,
    DeleteQuestionForm
)
from app.questions import bp


@bp.route("/")
@bp.route("/index")
@login_required
def list_questions():
    """list_questions 
        
    This view function deals with Question adding.
    It allows us to view the Questions, edit, delete add annc button.
    
    """
    questions = Question.get_all()

    kw = {
        "title" : "All Questions",
        # "username" : current_user.username,
        "questions" : questions
    }

    return render_template("questions/list.html", **kw)


@bp.route("/add", methods=['GET', 'POST'])
@login_required
def add_question():
    """add_Questions 
    
    GUI for adding Questions
    """
    msg = ""
    form = AddQuestionForm()

    if form.validate_on_submit():
        ann = Question(
            text = form.text.data
        )
        db.session.add(ann)
        db.session.commit()
        msg = "Success! Question added."

    kw = {
        "title" : "Add Question",
        "form" : form,
        "msg" : msg, 
        # "username" : current_user.username
    }

    return render_template('questions/edit.html', **kw)

@bp.route("/<int:question_id>/edit", methods=['GET', 'POST'])
@login_required
def edit_question(question_id: int):
    """edit_questions

    Allows editing of questions

    Args:
        question_id (int): ID in database of Questions
    """
    msg = ""

    ann = Question.query.filter_by(id=question_id).first_or_404()
    ann_name = True
    form = EditQuestionForm(obj=ann)

    if form.validate_on_submit():
        ann.text = form.text.data
        db.session.commit()
        msg = "Success! Page updated."
        flash(msg)
        return redirect(url_for("questions.list_questions"))
    
    kw = {
        "title" : f"Editing",
        "form" : form,
        "ann_name" : ann_name, 
        "msg" : msg, 
        # "username" : current_user.username
    }

    return render_template('questions/edit.html', **kw)

@bp.route("/<int:question_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_question(question_id: int):
    """delete_Question
    
    Deletes the Questions, given an id

    Args:
        Question_id (int): ID in database of Questions
    """
    msg = ""

    ann = Question.query.filter_by(id=question_id).first_or_404()
    ann_name = True
    form = DeleteQuestionForm(obj=ann)

    if form.validate_on_submit():
        if form.confirmation.data.lower() == "i am sure":
            db.session.delete(ann)
            db.session.commit()
            msg = "Success! Question deleted."
            flash(msg)
            return redirect(url_for("questions.list_questions"))
        else:
            msg = "Type 'I am sure' to proceed"

    kw = {
        "title" : f"Deleting '{ann_name}'",
        "form" : form,
        "ann_name" : ann_name, 
        "msg" : msg, 
        # "username" : current_user.username
    }

    return render_template('questions/delete.html', **kw)