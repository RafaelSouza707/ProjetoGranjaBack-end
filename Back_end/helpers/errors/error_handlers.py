from flask import jsonify
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from helpers.errors.exceptions import AppError


def register_error_handlers(app):

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({
            "error": {
                "message": error.message,
                "type": error.error_type,
                "status": error.status_code
            }
        }), error.status_code


    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return jsonify({
            "error": {
                "message": "Registro já existente ou violação de relacionamento",
                "type": "INTEGRITY_ERROR",
                "status": 409
            }
        }), 409


    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        return jsonify({
            "erro": "Erro de banco de dados"
        }), 500


    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            "erro": "Rota não encontrada"
        }), 404


    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({
            "erro": "Método não permitido"
        }), 405


    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception(error)

        return jsonify({
            "error": {
                "message": "Erro interno no servidor",
                "type": "INTERNAL_ERROR",
                "status": 500
            }
        }), 500