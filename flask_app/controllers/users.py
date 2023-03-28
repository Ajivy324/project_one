from flask import render_template,request,redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.sighting import Sighting
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add', methods=['POST'])
def add_user():
    if User.validate_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "fname": request.form["fname"],
            "lname" : request.form["lname"],
            "email" : request.form["email"],
            "password" : pw_hash,
            "confirm_password" : request.form["confirm_password"]
            }
        User.save(data)
        
        flash('Thank you for registering', "registration")
        return redirect('/')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form['email'])
    if not user or bcrypt.check_password_hash(user.password, request.form['password']) == False:
        flash('INVALID CREDENTIALS', "login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def all_sightings():
    if 'user_id' not in session:
        return redirect('/')
    sightings = Sighting.view()
    return render_template('dashboard.html', all_sightings = sightings, user = User.get_by_id(session['user_id']))

@app.route('/show/<int:id>')
def read_one(id):
    return render_template("view(one)_sighting.html", each_sighting=Sighting.get_by_id({"id" : id}),user = User.get_by_id(session['user_id']))




@app.route('/logout')
def logout():
    flash('Thank you for visting', "login")
    session.clear()
    return redirect('/')

@app.route('/delete/<int:user_id>')
def delete_sighting(user_id):
    Sighting.delete(user_id)
    return redirect("/dashboard")