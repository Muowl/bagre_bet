from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Usuario
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_secreta'  # Necessária para usar flash messages

db.init_app(app)

# Rota para cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        repetir_senha = request.form.get('repetir_senha')
        
        if senha != repetir_senha:
            flash("As senhas não coincidem!")
            return render_template('cadastro.html')

        novo_usuario = Usuario(nome=nome, email=email)
        novo_usuario.set_senha(senha)
        
        try:
            db.session.add(novo_usuario)
            db.session.commit()
            flash("Cadastro realizado com sucesso!")
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash("Nome ou E-mail já cadastrado!")
            return render_template('cadastro.html')
    
    return render_template('cadastro.html')

# Rota para login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_senha(senha):
            flash("Login efetuado com sucesso!")
            # Aqui você pode definir a sessão do usuário ou redirecionar para um dashboard
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciais inválidas. Tente novamente.")
            return render_template('login.html')

    return render_template('login.html')

# Rota exemplo para dashboard (página principal após login)
@app.route('/dashboard')
def dashboard():
    return "Bem-vindo ao dashboard!"

# Nova rota para visualização dos dados dos usuários
@app.route('/dados')
def dados():
    usuarios = Usuario.query.all()
    return render_template('dados.html', usuarios=usuarios)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas definidas
    app.run(debug=True)
