from flask import session
import uuid# usado para gerar IDs únicos (uuid4
#def são METODOS
class Usuario:
    
    def __init__(self, nome, cpf_limpo, email, idade, senha, cargo="comum"):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.cpf = cpf_limpo
        self.email = email
        self.idade = int(idade)
        self.senha = senha
        self.cargo = cargo

    def eh_maior_de_idade(self):
        return self.idade >= 18
    
    def eh_admin(self):
        return self.cargo == "admin"
        
    def to_dict(self):
        return {
                "id" : self.id,
                "nome" : self.nome,
                "cpf" : self.cpf,
                "email" : self.email,
                "idade" : self.idade,
                "senha" : self.senha,
                "cargo" : self.cargo
            }
    
class SessaoUsuario:
    @staticmethod
    def login(usuario_dict):
        session.clear()
        session["usuario_id"] = str(usuario_dict.get("id"))
        session["usuario_cpf"] = str(usuario_dict.get("cpf"))
        session["cargo"] = usuario_dict.get("cargo", "comum")
        session["usuario_nome"] = usuario_dict.get("nome", "Usuário")

    @staticmethod
    def logout():
        session.clear()

    @staticmethod
    def esta_logado():
        return "usuario_id" in session

    @staticmethod
    def eh_admin():
        return session.get("cargo") == "admin"

    @staticmethod
    def obter_cpf():
        return session.get("usuario_cpf", "")