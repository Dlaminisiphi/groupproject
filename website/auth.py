from flask import Blueprint,render_template, request, flash

auth=Blueprint('auth',__name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    data=request.form
    print(data)
    return render_template("login.html")

@auth.route('/admin', methods=['GET','POST'])
def admin():
    data=request.form
    print(data)
    return render_template("Admin_login.html")

@auth.route('/log-out')
def logout():
    return "log out"

@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    #Get user data from sign up page
    if request.method== 'POST':
        email=request.form.get('email')
        name=request.form.get('name')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        #Valadate information by user
        if len(email)<=4:
            flash(' not a valid email ', category='error')
        
        elif len(name)<=2:
            flash(' Name must be more than 2 charecters ', category='error')

            
        
        elif password1 != password2:
            flash(' passwords do not match ', category='error')
        
        elif len(password1)< 7:
            flash(' password must be more than 7 chatecters ', category='error')
        else:
            flash(' acount created! ', category='success')
            
    return render_template("sign_up.html")

