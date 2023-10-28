from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, IntegerField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from flask import current_app

from app.models import Shop


class ShopForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    street = StringField("Street")
    city = StringField("City")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Add shop", name="shop_form")
    
    
class ItemForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    shop = SelectField("Shop*", validators=[DataRequired()])#,
                        # choices=[(1, "Tempus Mauris Erat Incorporated"),
                                #  (2, "A Magna Ltd")],
                        # coerce=int)
    receipt_nr = StringField("Receipt Nr")
    # numeric fields optional by default
    amount = IntegerField("Amount", validators=[Optional()])
    price_per_piece = FloatField("Price per piece", validators=[Optional()])
    comment = StringField("Comment")
    purchase_date = DateField("Purchase date*", validators=[DataRequired()])
    warranty_months = IntegerField("Warranty length (months)*", validators=[DataRequired()])
    submit = SubmitField("Add item", name="item_form")
    
    def __init__(self):
        super(ItemForm, self).__init__()
        self.shop.choices = self.get_shop_records()
        self.shop.coerce = int
        
    def get_shop_records(self):
        with current_app.app_context():
            shops = Shop.query.all()
            return [(int(shop.id), shop.name) for shop in shops]
        
