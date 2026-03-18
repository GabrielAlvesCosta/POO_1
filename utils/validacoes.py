import re

def validar_formato_cpf(cpf: str) -> bool:

        padrao = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"
        if not cpf:
                return False
        return re.match(padrao, cpf) is not None

def sanitizar_cpf(cpf: str) -> str:
        if not cpf:
                return ""
        
        return re.sub(r"[.\-]", "", cpf)