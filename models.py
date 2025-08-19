from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# -------------------
# Usuário
# -------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relacionamento: usuário pode ter várias medições
    readings = db.relationship("Reading", backref="user", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"

# -------------------
# Medição de Glicemia
# -------------------
class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float, nullable=False)  # valor da glicemia
    when = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # data/hora
    note = db.Column(db.String(200))  # observações opcionais
    status = db.Column(db.String(50), nullable=False, default="Normal")  # status do diagnóstico
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<Reading {self.value} mg/dL — {self.status}>"
