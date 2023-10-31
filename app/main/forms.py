from datetime import date
from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, IntegerField, SelectField, StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


class ShopForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    street = StringField("Street")
    city = StringField("City")
    zip_code = StringField("Zip Code")
    submit = SubmitField("Add shop", name="shop_form")
    
    
class ItemForm(FlaskForm):
    name = StringField("Name*", validators=[DataRequired()], render_kw={"autofocus": True})
    shop = SelectField("Shop*", validators=[DataRequired()])#,
    receipt_nr = StringField("Receipt Nr")
    amount = IntegerField("Amount", validators=[Optional(),
                                                NumberRange(min=1,)])
    # price_per_piece_pattern = r'^(?:\d+|\d*\.\d+)$'
    price_per_piece = DecimalField("Price per piece",
                                   validators=[Optional(),
                                               NumberRange(min=0,)])
    comment = StringField("Comment")
    purchase_date = DateField("Purchase date*",
                              validators=[DataRequired()],
                              default=date.today())
    warranty_months = IntegerField("Warranty length (months)*",
                                   validators=[DataRequired(), NumberRange(min=1,)],
                                   default=12)
    
    def __init__(self, shop_choices):
        super(ItemForm, self).__init__()
        self.shop.choices = shop_choices
        self.shop.coerce = int


class AddItemForm(ItemForm):
    submit = SubmitField("Add item", name="add_item_form")
    
    
class EditItemForm(ItemForm):
    submit = SubmitField("Update Record", name="edit_item_form")
    

        