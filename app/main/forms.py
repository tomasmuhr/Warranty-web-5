from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


# class ContactForm(FlaskForm):
#     message = TextAreaField("Your Message", validators=[DataRequired()],
#                             render_kw={"autofocus": True})
#     submit = SubmitField("Send message", name="send_message")
    

class ShopForm(FlaskForm):
    pass
    # TODO
    

class WarrantyForm(FlaskForm):
    pass
    # TODO