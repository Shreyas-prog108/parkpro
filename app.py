from flask import Flask,redirect,url_for,render_template,request,session,flash
from models import db,User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config, config
import os
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import user_registration_form,user_login_form
from admin_dashboard import admin_dash
from user_dashboard import user_dash



app=Flask(__name__)
# Load environment-based configuration
env = os.getenv('FLASK_ENV', 'development')
config_class = config.get(env, config['development'])
app.config.from_object(config_class)
db.init_app(app)
migrate = Migrate(app, db)
login_manager=LoginManager(app)
login_manager.login_view="login"
app.register_blueprint(admin_dash)
app.register_blueprint(user_dash)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        e_mail = request.form.get("email","").strip()
        pass_word = request.form.get("password","").strip()
        if not e_mail or not pass_word:
            flash("Email and password are required!", "danger")
            return render_template("login.html")
        
        usr = User.query.filter_by(email=e_mail).first()
        if usr and check_password_hash(usr.password, pass_word): 
            login_user(usr)
            flash('Welcome to Parkpro!', "success")
            if usr.role == 'admin':
                return redirect(url_for("admin_dash.dash"))
            return redirect(url_for("user_dash.dash"))
        flash('Invalid login credentials!')
    if current_user.is_authenticated:
        flash(f"You are already logged in as {current_user.name}!", "info")
        return redirect(url_for("user_dash.dash"))
    
    return render_template("login.html")


        
@app.route("/register", methods=["GET","POST"])
def register():
    form = user_registration_form()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        exist_usr = User.query.filter_by(email=email).first()
        if exist_usr:
            flash("Account already exists! Please log in.", "info")
            return redirect(url_for("login"))
        
        new_usr = User(
            email=email,
            password=generate_password_hash(password),
            name=form.name.data,
            pincode=form.pincode.data,
            address=form.address.data
        )
        db.session.add(new_usr)
        db.session.commit()
        flash("You are now in Parkpro Family!", "success")
        return redirect("/login")
    return render_template("register.html", form=form)





@app.route("/logout")
@login_required
def logout(): 
    logout_user()
    flash("Please login to continue!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)