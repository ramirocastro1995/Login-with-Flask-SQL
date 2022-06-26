from flask import Flask, redirect, url_for, request , render_template , session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes = 5)

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/')
def test():
    return render_template("index.html")

@app.route('/view')
def view():
    return render_template("view.html", values = users.query.all())


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST" :
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by().first()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()




        flash("Login correcto!")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Ya estas logueado")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by().first()
            found_user.email = email
            db.session.commit()
            flash("El email fue guardado")
        else:
            if "email" in session:
                email = session["email"]
        
        return render_template("user.html", email=email)
 
    else:
        flash("No estas logueado")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    flash("Lograste desloguearte correctamente", "info")
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))

@app.route('/delete')
def delete():
    if 'user' in session and 'email' in session:
        user = session['user']
        email = session['email']
        users.query.filter_by(name=user).delete()
        users.query.filter_by(email=email).delete()
        db.session.commit()
        flash('Record deleted successfully!')
    elif 'user' in session and 'email' not in session:
        user = session['user']
        if not users.query.filter_by(name=user).first():
            flash('Unable to delete since there is no record found!')
        else:
            users.query.filter_by(name=user).delete()
            db.session.commit()
            flash('Record deleted successfully!')
    else:
        flash('Unable to delete record!')
    return redirect(url_for('user'))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)