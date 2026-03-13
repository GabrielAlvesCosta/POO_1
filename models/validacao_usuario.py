import re

class ValidacaoCadastro:

    def __init__(self, form_data, usuarios):
        self.dados = form_data
        self.usuarios = usuarios
        self.erros = []

    def validar(self):
        self._validar_idade()
        self._validar_cpf()
        self._validar_unicidade()

        return len(self.erros) == 0
    
    def _validar_idade(self):
        try:
            idade = int(self.dados.get("idade",0))

            if idade < 18:
                self.erros.append("Usuário deve ter mais que 18 anos!")

        except:
            self.erros.append("Idade Inválida!")