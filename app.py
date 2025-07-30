from flask import Flask,redirect,url_for,render_template,request,session,flash
from models import db,User
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import login_user,logout_user,login_required,LoginManager,current_user
from forms import user_registration_form,user_login_form
from admin_dashboard import admin_dash
from user_dashboard import user_dash



app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
login_manager=LoginManager(app)
login_manager.login_view="login"
app.register_blueprint(admin_dash)
app.register_blueprint(user_dash)

@login_manager.user_loader
def load_user(user_id):
    print(f"🔄 Loading User ID: {user_id}")
    user = User.query.get(int(user_id))
    print(f"✅ Loaded User: {user}")
    return user

@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        e_mail=request.form.get("email","").strip()
        pass_word=request.form.get("password","").strip()
        if not e_mail or not pass_word:
            flash("Email and password are required!","danger")
            return render_template("login.html")
        usr=User.query.filter_by(email=e_mail).first()
        if usr and pass_word:
            login_user(usr)
            flash('Welcome to Parkpro!',"success")
            if usr.role=='admin':
                return redirect(url_for("admin_dash.dash"))
            return redirect(url_for("user_dash.dash"))
        flash('Invalid login credentials!')
        print("❌ Invalid credentials!")
    if current_user.is_authenticated:
            flash(f"You are already logged in as {current_user.name}!","info")
            return redirect(url_for("user_dash.dash"))
    return render_template("login.html")
        
@app.route("/register",methods=["GET","POST"])
def register():
    form=user_registration_form()
    print("📩 Form Submitted:",request.method)
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        hashed_pass=password
        exist_usr=User.query.filter_by(email=email).first()
        if exist_usr:
            flash("Account already exists! Please log in.","info")
            return redirect(url_for("login"))
        new_usr=User(email=form.email.data,password=hashed_pass,name=form.name.data,pincode=int(form.pincode.data),address=form.address.data)
        db.session.add(new_usr)
        try:
            db.session.commit()
            flash("You are now in Parkpro Family!","success")
            print("✅ User registered successfully!")
            return redirect("/login")
        except Exception as e:
            db.session.rollback()
            flash("Something went wrong! Try again.","danger")
            print("Error committing to DB:",e)
    else:
        print("Form errors:",form.errors)
    return render_template("register.html", form=form)




@app.route("/logout")
@login_required
def logout(): 
    logout_user()
    flash("Please login to continue!")
    return redirect(url_for("login"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        admin_email="23f3001837@ds.study.iitm.ac.in"
        admin=User.query.filter_by(email=admin_email).first()
        if not admin:
            admin=User(
                name="SuperUser",
                email=admin_email,
                password="23f3001837_iitm",
                role="admin",
                pincode=233001,
                address="Harishankari,Ghazipur,U.P."
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created!")
        else:
            print("ℹ️ Admin user already exists.")
    app.run(debug=True)