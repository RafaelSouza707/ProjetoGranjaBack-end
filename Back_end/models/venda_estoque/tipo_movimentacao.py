from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String

from helpers.database import db


class TipoMovimentacao(db.Model):
    __tablename__ = "tipo_movimentacao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False
    )

    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(
        "MovimentacaoEstoque",
        back_populates="tipo_movimentacao"
    )