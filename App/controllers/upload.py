import os, string, random
from werkzeug.utils import secure_filename


def random_string():
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))


def store_file(file):
  upload_dir = os.path.join('uploads')
  if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
  extension = os.path.splitext(file.filename)[1]
  newname = secure_filename(random_string() + extension)
  file.save(os.path.join('uploads', newname))
  return newname


def remove_file(filename):
  try:
    os.remove(os.path.join('App/uploads', filename))
  except:
    print('file already Deleted')