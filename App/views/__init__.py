# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .apartment import apartment_views
from .auth import auth_views
from .admin import setup_admin
from .upload import upload_views



views = [user_views, index_views, apartment_views, auth_views,upload_views] 
# blueprints must be added to this list