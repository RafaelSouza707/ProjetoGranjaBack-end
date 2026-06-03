from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, CHAR

from helpers.database import db


class Sexo(db.Model):
    __tablename__ = "sexo"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    nome: Mapped[str] = mapped_column(
        CHAR(1),
        unique=True,
        nullable=False
    )

    funcionarios: Mapped[list["Funcionario"]] = relationship(
        "Funcionario",
        back_populates="sexo"
    )