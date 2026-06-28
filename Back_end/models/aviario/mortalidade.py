from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    BigInteger,
    Identity,
    ForeignKey,
    Integer,
    Date
)

from helpers.database import db

class Mortalidade(db.Model):
    __tablename__ = "mortalidade"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    lote_frango_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lote_frango.id", ondelete="CASCADE"),
        nullable=False
    )

    data: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )

    quantidade_mortes: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    lote_frango: Mapped["LoteFrango"] = relationship(
        "LoteFrango",
        back_populates="mortalidades"
    )