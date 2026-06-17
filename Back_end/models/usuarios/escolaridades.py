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

    funcionario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("funcionario.id", ondelete="CASCADE"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    funcionario: Mapped["Funcionario"] = relationship(
        "Funcionario",
        back_populates="escolaridades"
    )