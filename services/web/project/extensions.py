"""
To avoid cyclic imports, instantiate extensions here.
Use this module to access them elsewhere in project, instead using `__init__.py`
"""


from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


csrf = CSRFProtect()


# cors = CORS(resources={r"/api/*": {"origins": "*"}})


login_manager = LoginManager()
