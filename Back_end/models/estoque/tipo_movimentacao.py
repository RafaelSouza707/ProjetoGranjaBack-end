from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String, ForeignKey

from helpers.database import db


class TipoMovimentacao(db.Model):
    __tablename__ = "tipo_movimentacao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="CASCADE"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(64),
        nullable=False
    )

    movimentacoes: Mapped[list["MovimentacaoEstoque"]] = relationship(
        "MovimentacaoEstoque",
        back_populates="tipo_movimentacao"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="tipos_movimentacoes"
    )