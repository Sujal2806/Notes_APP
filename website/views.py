from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note')

        if len(note.strip()) < 1:
            flash('Note cannot be empty!', category='error') 
        else:
            new_note = Note(data=note.strip(), user_id=current_user.id)  
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note_data = json.loads(request.data)
    note_id = note_data.get('noteId')
    note = Note.query.get(note_id)

    if note and note.user_id == current_user.id:
        db.session.delete(note)
        db.session.commit()
        return jsonify({"success": True, "message": "Note deleted successfully!"})

    return jsonify({"success": False, "message": "Unauthorized action!"}), 403
