from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Identity, ForeignKey

from helpers.database import db


class RolePermissao(db.Model):
    __tablename__ = "role_permissao"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(start=1),
        primary_key=True
    )

    role_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("role.id", ondelete="CASCADE"),
        nullable=False
    )

    permissao_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("permissao.id", ondelete="CASCADE"),
        nullable=False
    )

    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="permissoes"
    )

    permissao: Mapped["Permissao"] = relationship(
        "Permissao",
        back_populates="roles"
    )