from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


# class ContactForm(FlaskForm):
#     message = TextAreaField("Your Message", validators=[DataRequired()],
#                             render_kw={"autofocus": True})
#     submit = SubmitField("Send message", name="send_message")
    

class AddShopForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    street = StringField("Street*", validators=[DataRequired()])
    city = StringField("City*", validators=[DataRequired()])
    zip_code = StringField("Zip Code*", validators=[DataRequired()])
    submit = SubmitField("Add shop", name="add_shop")
    

class AddItemForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    shop = SelectField("Shop*",
                        choices=[("todo1", "TODO1"), ("todo2", "TODO2")],
                        coerce=str, validators=[DataRequired()])
    receipt_nr = StringField("Receipt Nr*", validators=[DataRequired()])
    amount = IntegerField("Amount*", validators=[DataRequired()])
    price_per_piece = FloatField("Price per piece*", validators=[DataRequired()])
    comment = StringField("Comment")
    warranty_months = IntegerField("Warranty months*", validators=[DataRequired()])
    purchase_date = DateField("Purchase date*", validators=[DataRequired()])
    submit = SubmitField("Add item", name="add_item")