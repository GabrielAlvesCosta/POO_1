from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import  generate_password_hash, check_password_hash
import re
# VEM DOS MODELS
from models.usuario import Usuario 
from models.repositorio import RepositorioUsuarios
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

    if request.method == "POST":
        nome = request.form.get("nome")
        cpf = request.form.get("cpf")
        email = request.form.get("email")
        idade = request.form.get("idade")
        senha = request.form.get("senha")
        cargo = request.form.get("cargo", "comum")

        if not senha:
            flash("A senha é obrigatória!", "erro")
            return redirect(url_for("auth.cadastrar_usuario"))
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

        cpf_limpo = sanitizar_cpf(cpf)

        if not validar_formato_cpf(cpf_limpo):
            flash("CPF invalido! Use o formato: 000.000.000-00", "erro")
            return redirect(url_for("auth.cadastrar_usuario"))
# UNICIDADE DO CPF
        if repo.cpf_existe(cpf_limpo):
            flash("CPF já cadastrado!", "erro")
            return redirect(url_for("auth.cadastrar_usuario"))
# CRIAÇÂO  OBJETO DE PERSISTENCIA
        senha_hash = generate_password_hash(senha)

        novo_usuario = Usuario(nome, cpf_limpo, email, idade, senha_hash, cargo)

        if repo.salva(novo_usuario):
            flash("Usuário Cadastrado com Sucesso!", "sucesso")
            return redirect(url_for("auth.login"))
        else:
            flash("Não foi possível cadastrar o Usuário!", "erro")
            return redirect(url_for("auth.cadastrar_usuario"))
    return render_template("cadastro-usuario.html")
# LOGIN
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        cpf_bruto = request.form.get("cpf", "")
        senha_digitada = request.form.get("senha", "")
        
        cpf_limpo = sanitizar_cpf(cpf_bruto)

        # --- INÍCIO DO RAIO-X (DEBUG) ---
        print("\n--- INICIANDO TENTATIVA DE LOGIN ---")
        print(f"1. CPF bruto vindo do HTML: '{cpf_bruto}'")
        print(f"2. CPF após sanitizar (buscar no banco): '{cpf_limpo}'")

        usuario = repo.buscar_por_cpf(cpf_limpo)

        if usuario:
            print(f"3. Usuário ENCONTRADO no banco! Nome: {usuario.nome}")
            print(f"4. Senha/Hash que está salva no banco: '{usuario.senha}'")
            
            senha_confere = check_password_hash(usuario.senha, senha_digitada)
            print(f"5. A senha digitada confere com o hash? {senha_confere}")
            
            if senha_confere:
                print("6. LOGIN BEM SUCEDIDO! Redirecionando...\n")
                session["id"] = usuario.id
                session["nome"] = usuario.nome
                session["cargo"] = usuario.cargo
                flash(f"Bem-vindo, {usuario.nome}!", "sucesso")
                return redirect(url_for("usuario.listar_usuarios"))
            else:
                print("6. FALHA: A senha não bateu.")
        else:
            print("3. FALHA: Nenhum usuário encontrado com este CPF exato no banco.")
        # --- FIM DO RAIO-X ---

        flash("CPF ou Senha inválidos!", "erro")
    return render_template("login.html")
# LOGOUT
auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso!", "sucesso")
    return redirect(url_for("auth.login"))