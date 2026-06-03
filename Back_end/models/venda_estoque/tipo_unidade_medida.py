from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String

from helpers.database import db


class TipoUnidadeMedida(db.Model):
    __tablename__ = "tipo_unidade_medida"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    sigla: Mapped[str] = mapped_column(
        String(8),
        unique=True,
        nullable=False
    )

    descricao: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    produtos: Mapped[list["Produto"]] = relationship(
        "Produto",
        back_populates="tipo_unidade_medida"
    )