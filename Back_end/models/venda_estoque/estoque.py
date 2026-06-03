from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Numeric,
    TIMESTAMP,
    func
)

from helpers.database import db


class Estoque(db.Model):
    __tablename__ = "estoque"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    produto_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("produto.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True
    )

    quantidade_atual = mapped_column(
        Numeric(15, 3),
        nullable=False,
        default=0
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    produto: Mapped["Produto"] = relationship(
        "Produto",
        back_populates="estoque"
    )