from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Email,Length,EqualTo

class user_login_form(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder": "Enter Email"})
    password=PasswordField("Password",validators=[DataRequired(),Length(min=6)],render_kw={"placeholder": "Enter Password"})
    submit=SubmitField("Login")

class user_registration_form(FlaskForm):
    name=StringField("Full Name",validators=[DataRequired(),Length(min=3,max=50)],render_kw={"placeholder":"Enter Full Name"})
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder":"Enter Email"})
    password=PasswordField("Password",validators=[DataRequired(),Length(min=6)],render_kw={"placeholder":"Enter Password"})
    confirm_pass=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")],render_kw={"placeholder":"Confirm Password"})
    pincode=StringField("Pin Code",validators=[DataRequired(),Length(min=4,max=10)],render_kw={"placeholder":"Enter Pin Code"})
    address=StringField("Address",validators=[DataRequired(),Length(min=5,max=255)],render_kw={"placeholder":"Enter Address"})    
    submit=SubmitField("Register")
