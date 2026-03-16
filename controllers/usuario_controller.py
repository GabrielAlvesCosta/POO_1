from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash 
from werkzeug.security import generate_password_hash

from models.repositorio import RepositorioUsuarios
from utils.validacoes import sanitizar_cpf

usuario_bp = Blueprint("auth", __name__)

repo = RepositorioUsuarios()

def _usuario_logado() -> bool:
    return "usuario_id" in session

def _eh_admin() -> bool:
    return session.get("usuaruo_cargo") == "admin"
# LISTAGEM
@usuario_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    if not _usuario_logado():
        flash("Você precisa estar logado!", "erro")
        return redirect(url_for("auth.login"))
    
    usuarios= repo.listar()

# BUSCAR POR NOME OU CPF
    busca = request.args.get("q", "").strip().lower()
    if busca:
        usuarios = [u for u in usuarios
                    if busca in u.nome.lower()
                    or busca in u.cpf.lower()]
# ORDENAR POR IDADE
    ordem = request.args.get("ordem", "")
    if ordem == "asc":
        usuarios = sorted(usuarios, key=lambda u: u.idade)
    elif ordem == "desc":
        usuarios = sorted(usuarios, key=lambda u: u.idade, reverse=True)
    
    return render_template(
        "usuarios.html",
        usuarios = usuarios, #FUNÇÂO = VARIAVEL
        total=len(usuarios),
        busca=busca,
        ordem=ordem,
        )

@usuario_bp.route("/usuarios/json", methods=["GET"])
def listar_usuarios_json():
    if not _usuario_logado():
        return jsonify({"erro" : "Não autorizado!"}), 401
    usuarios =  repo.listar()
    return jsonify({u.to_ditc() for u in usuarios})
# EXCLUSÂO
@usuario_bp.route("/usuarios/deletar", methods=["POST"])
def deletar_usuario():
    if not _usuario_logado():
        flash("Não autorizado!", "erro")
        return redirect(url_for("auth.login"))
    
    if not _eh_admin():
        flash("Apenas administradores podem excluir!", "erro")
        return redirect(url_for("usuario.listar_usuarios"))
    
    cpf = request.form.get("cpf")
    if not cpf:
        flash("CPF necessario para exclusão!", "erro")
        return redirect(url_for("usuario.listar_usuarios"))
    
    if repo.deletar(cpf):
        flash("Usuario removido com sucesso!", "sucesso")
    else:
        flash("Erro ao deletar o usuário!", "erro")

    return redirect(url_for("usuario.listar_usuarios"))