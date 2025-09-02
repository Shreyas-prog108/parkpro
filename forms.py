from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Email,Length,EqualTo,Regexp,NumberRange

class user_login_form(FlaskForm):
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder": "Enter Email"})
    password=PasswordField("Password",validators=[DataRequired(),Length(min=6)],render_kw={"placeholder": "Enter Password"})
    submit=SubmitField("Login")

class user_registration_form(FlaskForm):
    name=StringField("Full Name",validators=[DataRequired(),Length(min=3,max=50)],render_kw={"placeholder":"Enter Full Name"})
    email=StringField("Email",validators=[DataRequired(),Email()],render_kw={"placeholder":"Enter Email"})
    password=PasswordField("Password",validators=[DataRequired(),Length(min=6)],render_kw={"placeholder":"Enter Password"})
    confirm_pass=PasswordField("Confirm Password",validators=[DataRequired(),EqualTo("password")],render_kw={"placeholder":"Confirm Password"})
    pincode=IntegerField("Pin Code",validators=[DataRequired(),NumberRange(min=100000,max=999999,message="Enter a valid 6-digit pincode")],render_kw={"placeholder":"Enter Pin Code"})
    address=StringField("Address",validators=[DataRequired(),Length(min=5,max=255)],render_kw={"placeholder":"Enter Address"})    
    submit=SubmitField("Register")

class vehicle_form(FlaskForm):
    vehicle_number = StringField(
        "Vehicle Number",
        validators=[
            DataRequired(message="Vehicle number is required"),
            Length(min=9, max=10, message="Vehicle number must be 9 or 10 characters"),
            Regexp(
                r'^[A-Z]{2}[0-9]{2}[A-Z]{1,3}[0-9]{4}$',
                message="Enter a valid Indian vehicle number (e.g., UP61A1234 or UP61ABC1234)"
            )
        ],
        render_kw={
            "placeholder": "UP61A1234",
            "style": "text-transform: uppercase;",
            "maxlength": "10",
            "class": "form-control vehicle-input"
        }
    )
    submit = SubmitField("Add Vehicle")
