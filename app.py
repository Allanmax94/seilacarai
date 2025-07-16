from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'segredo_do_allan'  # usado para proteger os dados da sessão

# Banco de dados SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Tabela de mensagens
class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    texto = db.Column(db.Text, nullable=False)

# Tabela de usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(100), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)

# Cria as tabelas no banco
with app.app_context():
    db.create_all()

# Rotas
@app.route("/")
def home():
    return render_template("index.html", nome="Allan")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato", methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form["nome"]
        mensagem = request.form["mensagem"]
        nova = Mensagem(nome=nome, texto=mensagem)
        db.session.add(nova)
        db.session.commit()
        return redirect("/mensagens")
    return render_template("contato.html")

@app.route("/mensagens")
def mensagens():
    mensagens = Mensagem.query.order_by(Mensagem.id.desc()).all()
    return render_template("mensagens.html", mensagens=mensagens)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]
        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and check_password_hash(user.senha_hash, senha):
            session["usuario"] = usuario
            return redirect("/painel")
        else:
            return "Usuário ou senha inválidos"
    return render_template("login.html")

@app.route("/painel")
def painel():
    if "usuario" in session:
        return render_template("painel.html", usuario=session["usuario"])
    return redirect("/login")

@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect("/")

# Criar usuário manualmente (temporário)
@app.route("/criar_usuario")
def criar_usuario():
    usuario = "allan"
    senha = "123"
    senha_segura = generate_password_hash(senha)
    novo = Usuario(usuario=usuario, senha_hash=senha_segura)
    db.session.add(novo)
    db.session.commit()
    return "Usuário criado: allan / 123"
