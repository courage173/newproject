from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_mysqldb import MySQL
import sqlalchemy as db
from passlib.hash import sha256_crypt
from sqlalchemy import create_engine





from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine("mysql+pymysql://root:pedro123@localhost/register")
db = scoped_session(sessionmaker(bind=engine))
appname = ""



app = Flask(__name__)

@app.route('/')
def home():

    return render_template("home.html")

#register form
@app.route('/register',methods =["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")


        username = request.form.get("username")


        faculty = request.form.get("faculty")
        department = request.form.get("department")
        project_supervisor = request.form.get("projectsupervisor")
        date_of_birth = request.form.get("date_of_birth")

        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute("INSERT INTO users(name, username,password) VALUES(:name,:username,:password)",
                       {"name":name,"username":username,"password":secure_password})
            db.commit()
            db.execute("INSERT INTO profile(department, faculty,project_supervisor,date_of_birth) VALUES(:department,:faculty,:project_supervisor,:date_of_birth)",
                       {"department": department, "faculty": faculty, "project_supervisor": project_supervisor,"date_of_birth": date_of_birth})
            db.commit()
            flash("you are registered and can log in", "success")
            return redirect(url_for('login'))
            flash("you are registered and can log in{register.username.data}","success")

            return redirect(url_for('login'))
        else:
            flash("password does not match","danger")

            return render_template("register.html")


    return render_template("register.html")

@app.route('/login', methods=["POST","GET"])
def login():



    if request.method == "POST":


        username = request.form.get("name")
        global appname
        appname =  request.form.get("name")
        print(appname)
        password = request.form.get("password")




        usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username": username}).fetchone()
        passwordata = db.execute("SELECT password FROM users WHERE username=:username",{"username": username}).fetchone()




        if usernamedata is None:
            flash("No username","danger")
            return render_template('login.html')
        else:
            for passwor_data in passwordata:
                if sha256_crypt.verify(password,passwor_data):
                    session["log"] = True
                    appname = username




                    return redirect(url_for('profile'))
                else:
                    flash("incorrect password","danger")
                    return render_template('login.html')



    return render_template("login.html")





@app.route('/profile', methods=["POST", "GET"])
def profile():
    print(appname)

    usernamedata = db.execute("SELECT username FROM users WHERE username=:username",{"username": appname}).fetchone()




    return render_template('profile.html',user = usernamedata)

@app.route('/logout')
def logout():
    session.clear()
    flash("you have been logged out!","success")

    return redirect(url_for('login'))
print(appname)

if __name__ == "__main__":
    app.secret_key = "1234567dailyweb"
    app.run(debug=True)
