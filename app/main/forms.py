from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


# class ContactForm(FlaskForm):
#     message = TextAreaField("Your Message", validators=[DataRequired()],
#                             render_kw={"autofocus": True})
#     submit = SubmitField("Send message", name="send_message")
    

class AddShopForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    description = TextAreaField("Shop description")
    street = StringField("Street*", validators=[DataRequired()])
    city = StringField("City*", validators=[DataRequired()])
    zip_code = StringField("Zip Code*", validators=[DataRequired()])
    submit = SubmitField("Add shop", name="add_shop")
    

class AddItemForm(FlaskForm):
    pass
    # TODO