from App.database import db
from .apartment import Apartment
from .user import User
from App.controllers.upload import store_file, remove_file


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=True)

    def __init__(self, file):
      self.filename = store_file(file)

    def remove_file(self):
      remove_file(self.filename)

    def get_url(self):
      return f'/uploads/{self.filename}'