from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Usuario
from sqlalchemy.exc import IntegrityError
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'chave_secreta'  # Necessária para usar flash messages e session

db.init_app(app)

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar esta página')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Decorator para verificar se o usuário é admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Por favor, faça login para acessar esta página')
            return redirect(url_for('login'))
        
        usuario = Usuario.query.get(session['usuario_id'])
        if usuario.nivel_acesso != 0:
            flash('Acesso restrito para administradores')
            return redirect(url_for('dashboard'))
            
        return f(*args, **kwargs)
    return decorated_function

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
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        usuario = Usuario.query.filter_by(email=email).first()
        
        if usuario and usuario.check_senha(senha):
            # Criar sessão para o usuário
            session['usuario_id'] = usuario.id_user
            session['usuario_nome'] = usuario.nome
            session['nivel_acesso'] = usuario.nivel_acesso
            
            flash("Login efetuado com sucesso!")
            return redirect(url_for('dashboard'))
        else:
            flash("Credenciais inválidas. Tente novamente.")
    
    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    flash("Logout efetuado com sucesso!")
    return redirect(url_for('login'))

# Rota para dashboard (página principal após login)
@app.route('/dashboard')
@login_required
def dashboard():
    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('dashboard.html', 
                          active_page='dashboard',
                          current_user=usuario)

# Rota para visualização dos dados dos usuários
@app.route('/dados')
@admin_required
def dados():
    usuario = Usuario.query.get(session['usuario_id'])
    usuarios = Usuario.query.all()
    return render_template('dados.html', 
                          active_page='dados',
                          current_user=usuario,
                          usuarios=usuarios)

# Rota para o perfil do usuário
@app.route('/perfil')
@login_required
def perfil():
    usuario = Usuario.query.get(session['usuario_id'])
    return render_template('perfil.html', 
                          active_page='perfil',
                          current_user=usuario)

# Página inicial - redireciona para login se não estiver logado
@app.route('/')
def index():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas definidas
        
        # Verifica se existe um usuário admin com email 'admin@bagre.bet'
        admin = Usuario.query.filter_by(email='admin@bagre.bet').first()
        if not admin:
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
        
    app.run(debug=True)
