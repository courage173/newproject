from flask import Flask,render_template,request,session,logging,url_for,redirect,flash
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

from passlib.hash import sha256_crypt

engine = create_engine("mysql+pymysql://root:pedro123@localhost/register")
db = scoped_session(sessionmaker(bind=engine))

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
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        secure_password = sha256_crypt.encrypt(str(password))

        if password == confirm:
            db.execute("INSERT INTO users(name, username,password) VALUES(:name,:username,:password)",
                       {"name":name,"username":username,"password":secure_password})
            db.commit()
            flash("you are registered and can log in","success")
            return redirect(url_for('login'))
        else:
            flash("password does not match","danger")

            return render_template("register.html")


    return render_template("register.html")

@app.route('/login', methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("name")
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

                    flash("you are now logged in","success")
                    return render_template('profile.html')
                else:
                    flash("incorrect password","danger")
                    return render_template('login.html')



    return render_template("login.html")
@app.route('/profile')
def profile():
    flash("You have been logged in","success")

    return render_template('profile.html')
@app.route('/logout')
def logout():
    session.clear()
    flash("you have been logged out!","success")

    return redirect(url_for('login'))

if __name__ == "__main__":
    app.secret_key = "1234567dailyweb"
    app.run(debug=True)
