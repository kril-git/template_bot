# from typing import TYPE_CHECKING
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# from sqlalchemy import ForeignKey
# from sqlalchemy import String
# from sqlalchemy import Enum
# from sqlalchemy import DateTime
# from sqlalchemy.sql import func
# from datetime import datetime
#
# from utils.ERoles import Roles
# from models.base import Base
#
# if TYPE_CHECKING:
#     from .user import User
#     from .catalog import Catalog
#
#
# class Orders_Products(Base):
#     __tablename__ = "orders_products"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
#     product_id: Mapped[int] = mapped_column(ForeignKey("catalog.id"))
#     extra_data: Mapped[str] = mapped_column(String(100))
#
#
# class Orders(Base):
#     __tablename__ = "orders"
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
#     # product_id: Mapped[int] = mapped_column(ForeignKey("catalog.id"))
#     date_create: Mapped[DateTime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )
#     date_update: Mapped[DateTime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
#     )
#     # user: Mapped["User"] = relationship(back_populates="orders")
#     product: Mapped[list["Orders_Products"]] = relationship(
#         secondary="orders_products", back_populates="orders"
#     )
#
#     def __str__(self) -> str:
#         return f"Orders(id = {self.id!r})"
#
#     def __repr__(self) -> str:
#         # return super().__repr__()
#         return str(self)
