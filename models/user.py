from sqlalchemy import String as db_string
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from utils.password_utils import hash, verify_password

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username : Mapped[str] = mapped_column(db_string(100), nullable=False)
    email : Mapped[str] = mapped_column(db_string(100), nullable=False)
    role : Mapped[str] = mapped_column(db_string(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(db_string(255), nullable=False)

    def set_password(self, password:str)-> None:
        self.password_hash = hash(password)

    def check_password(self, password:str)-> bool:
        return verify_password(password, self.password_hash)
    