from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class ShopForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    street = StringField("Street")
    city = StringField("City")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Add shop", name="shop_form")
    
    
class ItemForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    # shop = SelectField("Shop*",
    #                     choices=[("todo1", "TODO1"), ("todo2", "TODO2")],
    #                     coerce=str, validators=[DataRequired()])
    shop = SelectField("Shop*", validators=[DataRequired()],
                        choices=[(1, "Tempus Mauris Erat Incorporated"),
                                 (2, "A Magna Ltd")],
                        coerce=int)
    receipt_nr = StringField("Receipt Nr")
    amount = StringField("Amount")
    price_per_piece = StringField("Price per piece") # TODO add only numeric values
    comment = StringField("Comment") # TODO add only numeric values
    purchase_date = DateField("Purchase date*", validators=[DataRequired()])
    warranty_months = IntegerField("Warranty months*", validators=[DataRequired()])
    submit = SubmitField("Add item", name="item_form")