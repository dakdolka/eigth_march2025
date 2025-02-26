from sqlalchemy import Boolean, Column, Table, Integer, String, MetaData, ForeignKey, and_, func, JSON, ARRAY, UniqueConstraint, Date, or_, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.dialects.postgresql import JSONB
from data.database import Base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql import func
import enum, datetime
from typing import Annotated, Optional 


class ModerationState(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'

class Woman(Base):
    __tablename__ = "woman"
    
    tg_id: Mapped[str] = mapped_column(primary_key=True)
    chat_id: Mapped[str]
    description: Mapped[str]
    reg_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    circles_reached: Mapped[int] = mapped_column(default=0)
    delivers: Mapped[list["Man"]] = relationship(back_populates="aim")
    
class Man(Base):
    __tablename__ = "man"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    
    woman_aim: Mapped[str] = mapped_column(ForeignKey("woman.tg_id"), nullable=True)
    
    circle: Mapped[list["Message"]] = relationship(back_populates="man")
    aim: Mapped["Woman"] = relationship(back_populates="delivers")
    
    
class Message(Base):
    __tablename__ = 'message'

    sender_tg_id: Mapped[int] = mapped_column(ForeignKey("man.tg_id"), primary_key=True)
    video_note_id: Mapped[int] = mapped_column(primary_key=True)
    moderation_state: Mapped[ModerationState] = mapped_column(nullable=True, default=ModerationState.PENDING)
    
    man: Mapped["Man"] = relationship(back_populates="circle")
