from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String

from helpers.database import db

class TipoRacao(db.Model):
    __tablename__ = "tipo_racao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    descricao: Mapped[str] = mapped_column(
        String(256),
        nullable=True
    )

    lotes_racao: Mapped[list["LoteRacao"]] = relationship(
        "LoteRacao",
        back_populates="tipo_racao"
    )