#this where standard routes are stored for the site(where users can access eg. homepage)
from flask import Blueprint, render_template ,flash ,jsonify, request , redirect , url_for
from flask_login import login_required,current_user
from .models import Note
from . import db
import json

views = Blueprint("views", __name__)#define a blueprint

@views.route('/', methods=['GET', 'POST'])#making a route
@login_required #this will go to the main page of our website so whatever is in home it will run
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category='success')
            
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['nodeId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit() 

    return jsonify({})
