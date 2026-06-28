from helpers.database import db
from helpers.exceptions import NotFoundError
from models.usuarios.usuario import Usuario

from dotenv import load_dotenv
load_dotenv()

import os

from werkzeug.security import generate_password_hash, check_password_hash

import jwt
from datetime import datetime, timezone, timedelta

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = "HS256"

class UsuarioService:

    @staticmethod
    def listar():
        return db.session.query(Usuario).all()
    
    
    @staticmethod
    def buscar_por_id(id):
        registro = db.session.get(Usuario, id)
        if not registro:
            raise NotFoundError("Registro não encontrado")
        
        return registro
    

    @staticmethod
    def login(email, senha):
        usuario = (
            db.session.query(Usuario)
            .filter(Usuario.email == email)
            .first()
        )

        if not usuario:
            raise NotFoundError("Usuário não encontrado")

        if not check_password_hash(usuario.senha, senha):
            raise NotFoundError("Senha incorreta")

        payload = {
            "user_id": usuario.id,
            "username": usuario.nome,
            "exp": datetime.now(timezone.utc) + timedelta(hours=12)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "token": token,
            "usuario": {
                "id": usuario.id,
                "nome": usuario.nome
            }
        }



    @staticmethod
    def criar(data):
        data_to_save = data.copy()

        senha_hash = generate_password_hash(data_to_save["senha"])

        data_to_save["senha"] = senha_hash

        novo_registro = Usuario(**data_to_save)
        
        db.session.add(novo_registro)
        db.session.flush()

        return novo_registro
    

    @staticmethod
    def atualizar(registro, data):
        for k, v in data.items():
            setattr(registro, k, v)

        return registro
    

    @staticmethod
    def deletar(registro):
        db.session.delete(registro)
