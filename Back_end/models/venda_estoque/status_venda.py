from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String

from helpers.database import db

class StatusVenda(db.Model):
    __tablename__ = "status_venda"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True
    )

    vendas: Mapped[list["Venda"]] = relationship(
        "Venda",
        back_populates="status_venda"
    )