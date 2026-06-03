from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey, String

from helpers.database import db


class Endereco(db.Model):
    __tablename__ = "endereco"

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

    cep: Mapped[str] = mapped_column(
        String(8),
        nullable=False
    )

    rua: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    numero: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    bairro_logradouro: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    cidade: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    funcionario: Mapped["Funcionario"] = relationship(
        "Funcionario",
        back_populates="enderecos"
    )