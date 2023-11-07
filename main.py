from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object('config')
SECRET_KEY = 'bq8ZSQd!.BB@'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

if __name__ == "__main__":
    app.run(debug=True)
    
    

