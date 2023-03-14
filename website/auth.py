from flask import Blueprint,render_template, request, flash, redirect, url_for, jsonify,session
from . import db
from .models import User,Report
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user,current_user
import json, smtplib, ssl
auth=Blueprint('auth',__name__)


#--------------------------------------------------------------------------USER LOG IN---------------------------------------------------------------------------------------------
@auth.route('/login', methods=['GET','POST'])
def login():

    #validate user data
    request.form=='POST'
    email= request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            flash('Logged in sucessfuly', category='success')
            login_user(user, remember=True)
            return redirect(url_for('auth.user_home_page'))
        
        else: flash('Incorect email or password ', category='error')


    return render_template("login.html", user= current_user)
 
#--------------------------------------------------------------------------ADMIN LOG IN---------------------------------------------------------------------------------------------
#Adm
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
#------------------------------------------------------------------------------USER HOME PAGE---------------------------------------------
@auth.route("/user_home_page", methods=['GET','POST'])
@login_required
def user_home_page():
   
   if   request.method== 'POST':

        name=request.form.get('name')
        email=request.form.get('email')
        message=request.form.get('message')

       
    return render_template("user_home_page.html", user=current_user )
#----------------------------------------------------------------BUTTONS IN HOME PAGE--------------------------------------------------------
@auth.route("/log_complaint", methods=['GET','POST'])
@login_required
def log_complaint():
    return redirect(url_for('auth.user_Page'))


@auth.route("/view_complaint/<int:user_id>", methods=['GET','POST'])
@login_required
def view_complaint(user_id):
    report=Report.query.all()
    user = User.query.get(user_id)
 
    
    return render_template("user_complaint.html", user=user)

#--------------------------------------------------------------------------USER PAGE TO LOG A REPORT---------------------------------------------------------------------------------------------
@auth.route('/user_page', methods=['GET','POST'])
@login_required
def user_Page():
    if  request.method== 'POST':
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
            new_complant= Report(placeof=placeof, blockof=blockof, problem=problem, user_id=current_user.id)
            db.session.add(new_complant)
            db.session.commit()
            flash('Complenant Sent !', category='success')
            return redirect(url_for('auth.user_home_page'))
    return render_template("user_page.html", user= current_user)
#--------------------------------------------------------------------------ADMIN PAGE---------------------------------------------------------------------------------------------
@auth.route('/admin_page', methods=['GET','POST'])
def admin_page():
        reports=Report.query.all()
        return render_template("admin_page.html", user= current_user,reports=reports)

@auth.route('/delete-report', methods=['POST'])
def delete_report():
    report = json.loads(request.data)  
    reportId = report['reportId']
    report = Report.query.get(reportId)
    if report:
        db.session.delete(report)
        db.session.commit()
    return jsonify({})

auth.route( '/send-report-by-email', methods=['POST'])
def send_email():
    user=json.loads(request.data)
    user_email = user['email']
    user = db.session.query(User).filter_by(email=user_email).first()
    if user:
        report_text = f"Report for {user.name}\n\n"
        try:
            sender_email = "flaskschoolproject@gmail.com"
            receiver_email = user_email
            password = "utgukowrlaewmccw"
            message = f"Subject: Report for {user.name}\n\n{report_text}"
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.encode('utf-8'))
        except Exception as e:
            flash("Failed to send the report by email: " + str(e), "error")
        else:
            flash("Report has been sent by email to " + user_email, "success")
    else:
        flash("Report not found or user does not have a report.", "error")
    


