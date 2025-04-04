from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from data.database import Base
import enum, datetime


class ModerationState(enum.Enum):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
class MenStatus(enum.Enum):
    OPEN = 'open'
    CLOSED = 'closed'

class Woman(Base):
    __tablename__ = "woman"
    
    tg_id: Mapped[str] = mapped_column(primary_key=True)
    name_sur: Mapped[str] 
    description: Mapped[str]
    reg_time: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.now())
    circles_reached: Mapped[int] = mapped_column(default=0)
    circles_possible: Mapped[int] = mapped_column(default=0)
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
    
    receiver_id: Mapped[int] = mapped_column(default=0)
    
    man: Mapped["Man"] = relationship(back_populates="circle")
    
class Service(Base):
    __tablename__ = "service"
    man_id: Mapped[int] = mapped_column(primary_key=True)
    