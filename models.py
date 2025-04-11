from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_user = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    nivel_acesso = db.Column(db.Integer, default=1)  # 0 = admin, 1 = usuário normal

    def set_senha(self, password):
        self.senha = generate_password_hash(password)
    
    def check_senha(self, password):
        return check_password_hash(self.senha, password)
