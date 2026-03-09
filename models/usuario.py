from flask import session
import uuid# usado para gerar IDs únicos (uuid4
#def são METODOS
class Usuario:
    
    def __init__(self, nome, cpf, email, idade, senha, cargo="comum"):
        self.id = str(uuid.uuid4())
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.idade = idade
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

    def logout_POO(self):
        session.clear(self)