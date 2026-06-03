from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String

from helpers.database import db

class TipoProduto(db.Model):
    __tablename__ = "tipo_produto"

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

    produtos: Mapped[list["Produto"]] = relationship(
        "Produto",
        back_populates="tipo_produto"
    )