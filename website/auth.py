from flask import Blueprint,render_template, request, flash, redirect, url_for
from . import db
from .models import User,report, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user,current_user


auth=Blueprint('auth',__name__)
#--------------------------------------------------------------------------USER LOG IN---------------------------------------------------------------------------------------------
@auth.route('/login', methods=['GET','POST'])
def login():

    #validate user data
    data=request.form=='POST'
    email= request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash('Logged in sucessfuly', category='success')
            login_user(user, remember=True)
            return redirect(url_for('auth.user_Page'))
        
        else: flash('Incorect password', category='error')
            
    else: flash('Email does not exist', category='error')


    return render_template("login.html", user= current_user)
 
#--------------------------------------------------------------------------ADMIN LOG IN---------------------------------------------------------------------------------------------
#Admin
@auth.route('/admin', methods=['GET','POST'])
def admin():
    #validate Admin dat
    if  request.method== 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        
        user = username=='admin' and password=='password123'
        if user:
            flash('logged in sucessfuly', category='success')
            return redirect(url_for('auth.admin_page'))
        
        else:
            flash('invalid details', category='error')

    return render_template("Admin_login.html", user= current_user,)



#--------------------------------------------------------------------------SIGN OUT---------------------------------------------------------------------------------------------
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))




#--------------------------------------------------------------------------USER SIGN UP---------------------------------------------------------------------------------------------
@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    #Get user data from sign up page
    if  request.method== 'POST':
        email=request.form.get('email')
        first_name=request.form.get('name')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        #Valadate information by user
        user = User.query.filter_by(email=email).first()
        if user:
            flash('user already exists', category='error')
        elif len(email)<=4:
            flash(' not a valid email ', category='error')
        
        elif len(first_name)<=2:
            flash(' Name must be more than 2 charecters ', category='error')

            
        
        elif password1 != password2:
            flash(' passwords do not match ', category='error')
        
        elif len(password1)< 7:
            flash(' password must be more than 7 chatecters ', category='error')
        else:
            new_user= User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            #adding to database
            db.session.add(new_user)
            db.session.commit()
            flash(' acount created! ', category='success')
            return redirect(url_for('views.home'))

            
    return render_template("sign_up.html", user=current_user )

#--------------------------------------------------------------------------USER PAGE TO LOG A REPORT---------------------------------------------------------------------------------------------
@auth.route('/user_page', methods=['GET','POST'])
@login_required
def user_Page():
    if   request.method== 'POST':
        placeof=request.form.get('PlaceOf')
        blockof=request.form.get('BlockOf')
        problem=request.form.get('Report_problem')

        if placeof=="":
            flash('place enter place', category='error')
        elif blockof=="":
            flash('place enter block', category='error')
        elif len(problem)<3:
            flash('please type a descrptive problem to help maintenace team', category='error')
        else:
            new_complant= report(placeof=placeof, blockof=blockof, problem=problem)
            db.session.add(new_complant)
            db.session.commit()
            flash('Complenant Sent !', category='success')
            return redirect(url_for('views.home'))



    return render_template("user_page.html", user= current_user)
#--------------------------------------------------------------------------ADMIN PAGE---------------------------------------------------------------------------------------------
@auth.route('/admin_page', methods=['GET','POST'])
def admin_page():
        reports=report.query.all()
        return render_template("admin_page.html", user= current_user,reports=reports )





