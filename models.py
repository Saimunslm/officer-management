from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Officer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    area = db.Column(db.String(100), nullable=False)
    territory = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Officer {self.name}>'

# Use app context to create tables
with app.app_context():
    db.create_all()
