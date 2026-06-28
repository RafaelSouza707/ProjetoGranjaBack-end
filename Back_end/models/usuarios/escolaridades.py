from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey, String

from helpers.database import db


class Escolaridade(db.Model):
    __tablename__ = "escolaridades"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    usuario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuario.id", ondelete="CASCADE"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    usuario: Mapped["Usuario"] = relationship(
        "Usuario",
        back_populates="escolaridades"
    )