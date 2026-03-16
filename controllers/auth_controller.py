from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import  generate_password_hash, check_password_hash
import re
# VEM DOS MODELS
from models.usuario import Usuario 
from models.repositorio import RepositorioUsuarios
from models.validacao_usuario import ValidacaoCadastro
from utils.validacoes import validar_formato_cpf, sanitizar_cpf
# BLUEPRINT agrupa rotas
auth_bp = Blueprint("auth", __name__)

repo = RepositorioUsuarios()
# PAGINA INICIAL 
@auth_bp.route("/")
def home():
    return render_template("index.html")
# CADASTRO
@auth_bp.route("/cadastro-usuario", methods=["GET", "POST"])
def cadastrar_usuario():
    if request.method == "GET":
        return render_template("cadastro-usuario.html")
    
    dados = request.form
    nome = request.form.get("nome")
    cpf_sujo = dados.get("cpf")
    cpf_limpo = re.sub(r'\D', '', cpf_sujo)
    email = request.form.get("email")
    idade = request.form.get("idade")
    senha = request.form.get("senha")
    senha_hash = generate_password_hash(senha)
    cargo = request.form.get("cargo", "comum")
# VALOR IDADE
    try:
        idade = int(request.form.get("idade", 0))
    except ValueError:
        flash("Idade invalida!", "erro")
        return redirect(url_for("auth.cadastrar_usuario"))
    
    if idade < 18:
        flash("Cadastro apenas para maiores de idade!", "erro")
        return redirect(url_for("auth.cadastrar_usuario"))
# VALIDAR CPF
    if not validar_formato_cpf(cpf_limpo):
        flash("CPF invalido! Use o formato: 000.000.000-00", "erro")
        return redirect(url_for("auth.cadastrar_usuario"))
# UNICIDADE DO CPF
    if repo.cpf_existe(cpf_limpo):
        flash("CPF já cadastrado!", "erro")
        return redirect(url_for("auth.cadastrar_usuario"))
# CRIAÇÂO  OBJETO DE PERSISTENCIA
    senha_hash = generate_password_hash(senha_hash)
    cpf_salvo = sanitizar_cpf(cpf_limpo)

    novo_usuario = Usuario(nome, cpf_salvo, email, idade, senha_hash, cargo)

    if repo.salva(novo_usuario):
        flash("Usuário Cadastrado com Sucesso!", "sucesso")
        return redirect(url_for("auth.login"))
    else:
        flash("Não foi possível cadastrar o Usuário!", "erro")
        return redirect(url_for("auth.cadastrar_usuario"))
# LOGIN
auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf_digitado = sanitizar_cpf(request.form.get("cpf", ""))
        senha        = request.form.get("senha", "")

        usuario = repo.buscar_por_cpf(cpf_digitado)

        if usuario and check_password_hash(usuario.senha, senha):
            session["id"] = usuario.id
            session["nome"] = usuario.nome
            session["cargo"] = usuario.cargo
            flash(f"Bem-vindo, {usuario.nome}!", "sucesso")
            return redirect(url_for("usuario.listar_usuarios"))
        
    flash("CPF ou Senha inválidos!", "erro")
    
    return render_template("login.html")
# LOGOUT
auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "sucesso")
    return redirect(url_for("auth.login"))