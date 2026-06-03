from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey, String, Date, Numeric, Boolean, TIMESTAMP, func
from helpers.database import db


class Funcionario(db.Model):
    __tablename__ = "funcionario"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    cargo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("cargo.id", ondelete="RESTRICT"),
        nullable=False
    )

    sexo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("sexo.id", ondelete="RESTRICT"),
        nullable=False
    )

    nome: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False
    )

    senha: Mapped[str] = mapped_column(
        String(256),
        nullable=False
    )

    data_nascimento: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    data_entrada: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    salario = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    ativo: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    cargo: Mapped["Cargo"] = relationship(
        "Cargo",
        back_populates="funcionarios"
    )

    sexo: Mapped["Sexo"] = relationship(
        "Sexo",
        back_populates="funcionarios"
    )

    enderecos: Mapped[list["Endereco"]] = relationship(
        "Endereco",
        back_populates="funcionario",
        cascade="all, delete-orphan"
    )

    escolaridades: Mapped[list["Escolaridade"]] = relationship(
        "Escolaridade",
        back_populates="funcionario",
        cascade="all, delete-orphan"
    )