from datetime import date
from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange, Regexp


class ShopForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    street = StringField("Street")
    city = StringField("City")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Add shop", name="shop_form")
    
    
class ItemForm(FlaskForm):
    price_pattern_regexp = r"^(?:\d+|\d*\.\d+)$"
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    shop = SelectField("Shop*", validators=[DataRequired()])#,
                        # choices=[(1, "Tempus Mauris Erat Incorporated"),
                                #  (2, "A Magna Ltd")],
                        # coerce=int)
    receipt_nr = StringField("Receipt Nr")
    # numeric fields optional by default
    amount = IntegerField("Amount", validators=[Optional()])
    price_per_piece = IntegerField("Price per piece",
                                   validators=[Regexp(price_pattern_regexp, message="Enter a valid number or floating-point number.")])
    comment = StringField("Comment")
    purchase_date = DateField("Purchase date*",
                              validators=[DataRequired()],
                              default=date.today())
    warranty_months = IntegerField("Warranty length (months)*",
                                   validators=[DataRequired(), NumberRange(min=1,)],
                                   default=12)
    submit = SubmitField("Add item", name="item_form")
    
    def __init__(self, shop_choices):
        super(ItemForm, self).__init__()
        self.shop.choices = shop_choices
        self.shop.coerce = int
        