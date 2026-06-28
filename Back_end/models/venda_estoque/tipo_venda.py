from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String, ForeignKey

from helpers.database import db

class TipoVenda(db.Model):
    __tablename__ = "tipo_venda"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    granja_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("granja.id", ondelete="RESTRICT"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True
    )

    vendas: Mapped[list["Venda"]] = relationship(
        "Venda",
        back_populates="tipo_venda"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="tipos_venda"
    )