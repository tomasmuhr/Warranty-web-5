from app import db
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)
#     password_hash = db.Column(db.String(128))
#     last_seen = db.Column(db.Date)#, default=datetime.utcnow)
#     dark_theme = db.Column(db.Integer)

#     def __repr__(self):
#         return f"<User {self.username}>"
    
#     def set_password(self, password):
#         self.password_hash = generate_password_hash(password)
        
#     def check_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def get_reset_password_token(self, expires_in=600):
#         return jwt.encode({"reset_password": self.id, "exp": time() + expires_in},
#                           current_app.config["SECRET_KEY"],
#                           algorithm="HS256")
        
#     def set_dark_theme(self, dark_theme):
#         self.dark_theme = dark_theme

#     @staticmethod
#     def verify_reset_password_token(token):
#         try:
#             id = jwt.decode(token,
#                             current_app.config["SECRET_KEY"],
#                             algorithms=["HS256"])["reset_password"]
#         except:
#             return

#         return User.query.get(id)
      



# class Message(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     # user_id = db.Column(db.Integer(), db.ForeignKey("user.id", name="fk_message_user_id"))
#     user_id = db.Column(db.Integer())
#     msg_datetime = db.Column(db.DateTime())
#     msg_text = db.Column(db.Text)
#     msg_username = db.Column(db.String(120))
#     msg_email = db.Column(db.String(120))
    
#     def __repr__(self):
#         return f"Message by {self.user_id}:\n{self.msg_text}"
       

# class FormerUser(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     former_id = db.Column(db.Integer())
#     former_username = db.Column(db.String(64))
#     former_email = db.Column(db.String(120))
#     deletion_date = db.Column(db.Date())

#     def __repr__(self):
#         return f"<Former user {self.username}, deleted on: {self.deletion_date}>"
    

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dark_mode = db.Column(db.Integer())
    

class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    street = db.Column(db.String(150))
    city = db.Column(db.String(64))
    zip_code = db.Column(db.String(10))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    shop_id = db.Column(db.Integer, db.ForeignKey("shop.id", name="fk_item_shop_id"))
    receipt_nr = db.Column(db.String(20))
    amount = db.Column(db.Integer)
    price_per_piece = db.Column(db.Integer)
    warranty_months = db.Column(db.Integer)
    comment = db.Column(db.String(255))
    dates_id = db.Column(db.Integer, db.ForeignKey("dates.id", name="fk_item_dates_id"))


class Dates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("item.id", name="fk_dates_item_id"))
    purchase_date = db.Column(db.Date())
    expiration_date = db.Column(db.Date())

        