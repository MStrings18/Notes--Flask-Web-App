from flask import Blueprint, render_template,request, flash,redirect,url_for
from flask_login import login_required,current_user
from .models import Note
from . import db

views=Blueprint('views',__name__)

@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method=='POST':
        note=request.form.get('note')
        if len(note)<1:
            flash("That's an empty note bub...", category='error')
        else:
            new_note=Note(data=note,user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!',category='success')
            return redirect(url_for('views.home'))
    return render_template("home.html",user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note_id = request.form.get('note_id')
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash('Note deleted!', category='success')
        else:
            flash('You do not have permission to delete this note.', category='error')
    else:
        flash('Note not found.', category='error')
    return redirect(url_for('views.home'))