from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String, ForeignKey

from helpers.database import db

class TipoProduto(db.Model):
    __tablename__ = "tipo_produto"

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
        String(64),
        nullable=False,
        unique=True
    )

    produtos: Mapped[list["Produto"]] = relationship(
        "Produto",
        back_populates="tipo_produto"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="tipos_produto"
    )