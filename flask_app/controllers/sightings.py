from flask import render_template,request,redirect, session, flash
from flask_app import app
from flask_app.models.sighting import Sighting
from flask_app.models.user import User
import datetime
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/dashboard/new')
def add_sighting_form():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('add_sighting.html', user = User.get_by_id(session['user_id']))

@app.route('/dashboard/add', methods=['POST'])
def add_sighting():
    if Sighting.validate_sighting(request.form):
        data = {
            "location": request.form["location"],
            "what_happend" : request.form["what_happend"],
            "number_of" : request.form["number_of"],
            "created_at" : request.form["created_at"],
            "user_id" : session['user_id']
            }
        Sighting.save(data)
        return redirect('/dashboard')
    return redirect('/dashboard/new')

@app.route('/edit/<int:id>')
def edit_page(id):

    if 'user_id' not in session:
        return redirect('/')
    
    data = {
        'id': id
    }
    
    each_sighting = Sighting.view_one(data)

    return render_template("edit.html", each_sighting = each_sighting, user = User.get_by_id(session['user_id']))

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if Sighting.validate_update(request.form):
        data = {
            'id': id,
            "location":request.form['location'],
            "what_happend": request.form['what_happend'],
            "number_of" : request.form["number_of"],
            "updated_at" : request.form['updated_at']
        }
        Sighting.update(data)
        return redirect("/dashboard")
    return redirect(f'/edit/{id}')


