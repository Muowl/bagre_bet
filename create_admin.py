"""
Script para criar um usuário administrador no Bagre Bet
Uso: python create_admin.py
"""

from flask import Flask
from models import db, Usuario

# Configuração básica da aplicação
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def create_admin():
    with app.app_context():
        # Verifica se existe um usuário admin com email 'admin@bagre.bet'
        admin = Usuario.query.filter_by(email='admin@bagre.bet').first()
        
        if admin:
            print(f"Usuário administrador já existe: {admin.nome} ({admin.email})")
            return
            
        # Cria o usuário admin caso não exista
        admin = Usuario(
            nome='Administrador',
            email='admin@bagre.bet',
            nivel_acesso=0,  # 0 = admin
            saldo=1000.0  # Saldo inicial para o admin
        )
        admin.set_senha('ademir')  # Define a senha como 'ademir'
        
        db.session.add(admin)
        db.session.commit()
        print('Usuário administrador criado com sucesso!')

if __name__ == '__main__':
    create_admin()