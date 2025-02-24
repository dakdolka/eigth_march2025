from sqlalchemy import Boolean, Column, Table, Integer, String, MetaData, ForeignKey, and_, func, JSON, ARRAY, UniqueConstraint, Date, or_, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from data.database import Base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
import enum, datetime
from typing import Annotated, Optional 

class Woman(Base):
    __tablename__ = "woman"
    
    tg_id: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
    reg_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    circles_reached: Mapped[int] = mapped_column(default=0)
    delivers: Mapped[list["Man"]] = relationship(back_populates="aim")
    
class Man(Base):
    __tablename__ = "man"
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(primary_key=True)
    
    aim: Mapped["Woman"] = relationship(back_populates="delivers")
    circle: Mapped[str] = mapped_column(default="")
    is_sent: Mapped[bool] = mapped_column(default=False)
    woman_aim: Mapped[str] = mapped_column(ForeignKey("woman.tg_id"))
    
    
    
    
    
    
    