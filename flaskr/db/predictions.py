import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean,ForeignKey

from flaskr.db.users import Users
from flaskr.db.games import Games
from flaskr.db.base_model import Model


class Predictions(Model):
    """Predictions"""
    __tablename__ = 'tbl_predictions'
    game = Column(UUID(as_uuid=True), ForeignKey('tbl_games.id'),primary_key=True)
    user = Column(String,ForeignKey('tbl_users.email'),primary_key=True)
    actual_score = Column(String,default=None)
    predicted_score = Column(String, nullable=False)
    points = Column(Integer,default=None)


    def __init__(self, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Pred({self.game + self.user})>"


