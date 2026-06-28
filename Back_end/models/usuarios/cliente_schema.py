from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, String, ForeignKey

from helpers.database import db


class Cliente(db.Model):
    __tablename__ = "cliente"

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
        String(128),
        nullable=False
    )

    cpf_cnpj: Mapped[str] = mapped_column(
        String(18),
        unique=True,
        nullable=False
    )

    telefone: Mapped[str] = mapped_column(
        String(20),
        nullable=True
    )

    email: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=True
    )

    enderecos: Mapped[list["Endereco"]] = relationship(
        "Endereco",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    vendas: Mapped[list["Venda"]] = relationship(
        "Venda",
        back_populates="cliente"
    )

    granja: Mapped["Granja"] = relationship(
        "Granja",
        back_populates="cliente"
    )