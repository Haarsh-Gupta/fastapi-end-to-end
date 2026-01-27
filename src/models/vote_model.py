from ..db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column , Integer , ForeignKey, CheckConstraint

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id" ,ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id" ,ondelete="CASCADE"), primary_key=True)
    vote = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint("vote IN (1, -1)", name="vote_value_check"),
    )