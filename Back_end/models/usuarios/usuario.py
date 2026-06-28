from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey, String, Date, Numeric, Boolean, TIMESTAMP, func
from helpers.database import db


class Usuario(db.Model):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    sexo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("sexo.id", ondelete="RESTRICT"),
        nullable=True
    )

    nome: Mapped[str] = mapped_column(
        String(128),
        nullable=False
    )

    cpf: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=True
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
        nullable=True
    )

    salario = mapped_column(
        Numeric(15, 2),
        nullable=True
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

    sexo: Mapped["Sexo"] = relationship(
        "Sexo",
        back_populates="usuarios"
    )

    enderecos: Mapped[list["Endereco"]] = relationship(
        "Endereco",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    escolaridades: Mapped[list["Escolaridade"]] = relationship(
        "Escolaridade",
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    granjas: Mapped[list["UsuarioGranja"]] = relationship(
        "UsuarioGranja",
        back_populates="usuario"
    )