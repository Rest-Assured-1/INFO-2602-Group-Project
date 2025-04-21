from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from App.models import User
from App.models import db
from App.models.landlord import Landlord
from App.models.tenant import Tenant


#Function to register a new user
def register_user(username, password, user_type):
    if User.query.filter_by(username=username).first():
        return None

    if user_type == 'landlord':
        user = Landlord(username=username, password=password)
    elif user_type == 'tenant':
        user = Tenant(username=username, password=password)
    else:
        user = User(username=username, password=password)

    db.session.add(user)
    db.session.commit()
    return user


#Function to login a user
def login(username, password):
  user = User.query.filter_by(username=username).first()
  if user and user.check_password(password):
    print("username", type(username))
    return create_access_token(identity=username)
  return None


def setup_jwt(app):
  jwt = JWTManager(app)
  @jwt.user_identity_loader
  def user_identity_lookup(identity):
    user = User.query.filter_by(username=identity).one_or_none()
    if user:
        print("id type",type(user.id))
        return str(user.id)
    return None


  @jwt.user_lookup_loader
  def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    print("type",type(identity))
    return User.query.get(identity)

  return jwt


def add_auth_context(app):
  @app.context_processor
  def inject_user():
      try:
          verify_jwt_in_request()
          user_id = get_jwt_identity()
          print("user_id",type(user_id))
          current_user = User.query.get(user_id)
          is_authenticated = True
      except Exception as e:
          print(e)
          is_authenticated = False
          current_user = None
      return dict(is_authenticated=is_authenticated, current_user=current_user)