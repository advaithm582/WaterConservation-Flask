import typing as t
import secrets
import string
import time
from datetime import timedelta
from datetime import datetime
from hashlib import md5

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from app import db, login

class User(UserMixin, db.Model):
    #:int: Integer ID
    id = db.Column(db.Integer, primary_key=True)
    #:str: Unique ID to prevent relogin on pwdreset
    unique_id = db.Column(db.String(32), index=True, unique=True)
    #:str: The name of user
    full_name = db.Column(db.String(128))
    #:str: Username
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    relogin_tokens = db.relationship('ReloginToken', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")
    roles = db.relationship('Role', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")
    water_profile = db.relationship('WaterConservation', backref='user', lazy='dynamic', cascade="all, delete, delete-orphan")
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def get_id(self) -> str:
        """get_id 
        
        Get ID for Flask-Login

        Returns:
            str: UniqueID
        """
        return self.unique_id

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def change_password(self, old_password: str, new_password: str) -> bool:
        """change_password 
        
        Changes the user's password, given the old one, and the new
        one. The password is changed iff the old one matches.

        Args:
            old_password (str): The previous password of the user.
            new_password (str): The new password of the user.

        Returns:
            bool: If the operation succeded or not.
        """
        if self.check_password(old_password):
            self.set_password(new_password)
            return True
        else:
            return False

    def generate_uid(self) -> None:
        """generate_uid 
        
        Generate or regenerate a UID for a user.
        """
        self.unique_id = ''.join(secrets.choice(string.ascii_letters 
            + string.digits) for i in range(32))

    def avatar(self, size):
        if self.email:
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                digest, size)
        else:
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
                "default", size)

    def get_name(self):
        if self.full_name:
            return self.full_name.split()[0]
        else:
            return self.username

    def get_roles(self) -> list[str]:
        """get_roles 
        
        Get all roles of current user

        Returns:
            list of str: List of roles
        """
        roles = self.roles
        list_of_str = list()
        for role in roles:
            list_of_str.append("{}:{}".format(
                role.category, role.scope))

        return list_of_str
    
    def can_do(self, category: str, scope:str="view") -> bool:
        """can_do 
        
        Whether user has a role.

        Args:
            category (str): Category
            scope (str, optional): Scope. Defaults to "view".

        Returns:
            bool: True when role exists else False
        """
        roleobj = self.roles.filter_by(category=category, 
                                       scope=scope).first()
        
        return bool(roleobj)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.unique_id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            unique_id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.filter_by(unique_id=unique_id).first()
    
    def is_suspended(self):
        return self.username.startswith("__")
        
    def suspend(self):
        self.username = "__" + self.username
        
    def activate(self):
        if self.is_suspended():
            self.username = self.username[2:]


@login.user_loader
def load_user(unique_id):
    """load_user 
    
    This function returns a unique string to identify users.

    Args:
        uid (str): The uniqe identifier

    Returns:
        User: User object
    """
    # return User.query.get(int(id))
    return User.query.filter_by(unique_id=unique_id).first()


# @identity_loaded.connect_via(app)
# def on_identity_loaded(sender, identity):
#     # Set the identity user object
#     identity.user = current_user

#     # Add the UserNeed to the identity
#     if hasattr(current_user, 'id'):
#         identity.provides.add(UserNeed(current_user.id))

#     # Assuming the User model has a list of roles, update the
#     # identity with the roles that the user provides
#     #if hasattr(current_user, 'roles'):
#     for role in current_user.get_roles():
#         identity.provides.add(RoleNeed(role))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    scope = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class ReloginToken(db.Model):
    token = db.Column(db.String(64), primary_key=True)
    ipaddr = db.Column(db.String(10))
    user_agent = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, *a, **kw) -> None:
        super().__init__(*a, **kw)
        self.generate_token()

    def generate_token(self) -> None:
        """generate_token
        
        Generate a token for a user.
        """
        self.token = ''.join(secrets.choice(string.ascii_letters 
            + string.digits) for i in range(32))

    def check(self, ipaddr: str, user_agent: str) -> bool:
        validity = (datetime.utcnow() - self.created_on) <= timedelta(minutes=30)
        # breakpoint()
        if self.ipaddr == ipaddr \
                and self.user_agent == user_agent and validity:
            return True
        else:
            return False

class WaterConservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    no_of_taps = db.Column(db.Integer, nullable=False)
    no_of_leaky_taps = db.Column(db.Integer, nullable=False)
    delta_leakage_per_min = db.Column(db.Integer, nullable=False)
    
    # Flow Rate
    avg_flow_rate = db.Column(db.Integer, nullable=False)
    time_to_wash_vessel = db.Column(db.Integer, nullable=False) #mins
    
    # RWH
    saved_using_rwh = db.Column(db.Integer, nullable=False) # in m^3, convert to litre
    
    total_water_used = db.Column(db.Integer, nullable=False)
    
    created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def calculate(self):
        self.total_water_used = (
            + (self.no_of_leaky_taps * self.delta_leakage_per_min * 1440 * 30) # per day *month
            + (self.avg_flow_rate * self.time_to_wash_vessel * 30) # per month
            - (self.saved_using_rwh * 1000)
            )


# class Announcement(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(64))
#     body = db.Column(db.String(500))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

#     @staticmethod
#     def get_all():
#         return Announcement.query.order_by(Announcement.timestamp.desc())

# class Topic(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     desc = db.Column(db.String(100000))
#     questions = db.relationship('Question', backref='topic', lazy='dynamic')

# class Question(db.Model):
#     #__tablename__ = "questions"
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(100000))
#     # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'))
#     answers = db.relationship('Option', backref='question', lazy='dynamic')
#     option_id = db.Column(db.Integer, db.ForeignKey('option.id'))

#     def __repr__(self):
#         return '<Question {}, options {}>'.format(self.text, \
#             (answer for answer in self.answers))

#     @staticmethod
#     def get_all():
#         return Question.query.order_by(Question.id.desc())

# class Option(db.Model):
#     #__tablename__ = "options"
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(100000))
#     # timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
#     # correct_qn = db.relationship('Question', backref='correct_a', lazy='dynamic')
#     def __repr__(self):
#         return '<Option {}>'.format(self.text)



# class Page(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     path = db.Column(db.String(200))
#     title = db.Column(db.String(64))
#     body = db.Column(db.String(500))
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#     def __repr__(self):
#         return '<Post {}>'.format(self.body)

#     @staticmethod
#     def get_all():
#         return Page.query.order_by(Page.timestamp.desc())
