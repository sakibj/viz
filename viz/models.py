from __init__ import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

"""
There will be options on a business card view to "connect to company" and also
"inherit info from company" as in sync the logo, email, contact, address, gallery
There should be pages such as view-company, view-user, view-my-card-directory, etc.
"""


class UserDB(db.Model):
    """User object stores all necessary information for a site user.
    """
    __tablename__ = 'users'
    username = db.Column(db.String(15), primary_key=True, index=True, nullable=False)
    img_id = db.Column(db.Integer, db.ForeignKey('images.img_id'))
    email = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50))
    pass_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.pass_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.pass_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'username': self.username})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = UserDB.query.get(data['username'])
        return user


class VizCardDB(db.Model):
    """Card object stores all necessary information for a card on the app
    card_id     : integer   -> primary key
    user_id     : string    -> owner of the card
    position    : string    -> position in the company
    address_id  : integer   -> foreignkey into address DB, company addr by default
    phone_num   : string    -> part of the contact info
    email       : string    -> part of the contact info
    company     : string    -> foreignkey into company DB
    logo_id     : integer   -> foreignkey into image DB, company logo by default
    gallery_id  : integer   -> foreignkey into gallery DB for images for the card
    type        : integer   -> 1 for public, 0 for private
    """
    __tablename__ = 'cards'
    card_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(15), db.ForeignKey('users.username'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.gallery_id'))
    logo_id = db.Column(db.Integer, db.ForeignKey('images.img_id'))
    position = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Integer, nullable=False)
    phone_num = db.Column(db.String(30))
    email = db.Column(db.String(50))


class UserDirectoryDB(db.Model):
    """User specific information regarding various business cards
    user_id     : integer   -> foreignkey to a user's profile
    card_id     : integer   -> foreignkey to a specific viz card
    address_id  : integer   -> foreignkey to the address of where these people met
    notes       : string    -> customized notes a user has about a specific card
    """
    __tablename__ = 'userdir'
    userdir_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(15), db.ForeignKey('users.username'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.card_id'), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    notes = db.Column(db.String(200))


class CompanyDB(db.Model):
    """Company info object
    """
    __tablename__ = 'companies'
    name = db.Column(db.String(50), primary_key=True, nullable=False)
    logo_id = db.Column(db.Integer, db.ForeignKey('images.img_id'))
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    gallery_id = db.Column(db.Integer, db.ForeignKey('galleries.gallery_id'))
    email = db.Column(db.String(50))
    phone_num = db.Column(db.String(30))


class GalleryDB(db.Model):
    """Gallery object to store a predetermined upper limit size of pictures for a card.
    """
    __tablename__ = 'galleries'
    gallery_id = db.Column(db.Integer, primary_key=True, nullable=False)
    image_1 = db.Column(db.Integer, db.ForeignKey('images.img_id'), nullable=False)
    image_2 = db.Column(db.Integer, db.ForeignKey('images.img_id'))
    image_3 = db.Column(db.Integer, db.ForeignKey('images.img_id'))
    image_4 = db.Column(db.Integer, db.ForeignKey('images.img_id'))
    image_5 = db.Column(db.Integer, db.ForeignKey('images.img_id'))


class ImageDB(db.Model):
    """Image database
    image_id    : integer   -> Unique identifier
    img_name    : string    -> Append to webserver/pathname/img_name for image lookup
    description : string    -> Basic description of image
    """
    __tablename__ = 'images'
    img_id = db.Column(db.Integer, primary_key=True, nullable=False)
    img_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(50))


class AddressDB(db.Model):
    """Address object to store necessary information. All cards have this.
    """
    __tablename__ = 'addresses'
    address_id = db.Column(db.Integer, primary_key=True, nullable=False)
    address1 = db.Column(db.String(50), nullable=False)
    address2 = db.Column(db.String(50))
    city = db.Column(db.String(25), nullable=False)
    state = db.Column(db.String(25), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    zip = db.Column(db.String(25), nullable=False)
