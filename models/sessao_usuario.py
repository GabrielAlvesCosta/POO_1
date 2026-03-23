#from flask import session
class SessaoUsuario:

    def __init__(self, session):
        self._session = session
    
    def iniciar(self, usuario):
        self._session["usuario_id"] = usuario["id"]
        self._session["usuario_nome"] = usuario["nome"]
        self._session["usuario_cargo"] = usuario["cargo", "comum"]
        self._session["usuario_cpf"] = usuario["cpf"]
    
    def logout(self):
        self._session.clear()
    
    def esta_logado(self):
        return "usuario_id" in self.session
    
    def eh_admin(self):
        return self._session.get("cargo") == "admin"
    
    def obter_cpf(self):
        return self.session.get("usuario_cpf", "")


    #@staticmethod
    #def login(usuario_dict):
        #session.clear()
        #session["usuario_id"] = str(usuario_dict.get("id"))
       #session["usuario_cpf"] = str(usuario_dict.get("cpf"))
        #session["cargo"] = usuario_dict.get("cargo", "comum")
        #session["usuario_nome"] = usuario_dict.get("nome", "Usuário")

    #@staticmethod
    #def logout():
        #session.clear()

    #@staticmethod
    #def esta_logado():
        #return "usuario_id" in session

    #@staticmethod
    #def eh_admin():
        #return session.get("cargo") == "admin"

    #@staticmethod
    #def obter_cpf():
        #return session.get("usuario_cpf", "")