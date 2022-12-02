from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, ForeignKey

from flaskr.db.base_model import Model


class Predictions(Model):
    """Predictions"""
    __tablename__ = 'tbl_predictions'
    user_email = Column(String, ForeignKey('tbl_users.email'), primary_key=True, index=True)
    game_id = Column(UUID(as_uuid=True), ForeignKey('tbl_games.id'), primary_key=True, index=True)
    actual_score = Column(String, default=None)
    predicted_score = Column(String, nullable=False)
    points = Column(Integer, default=None)
    prediction_insert_date = Column(String, nullable=True)
    prediction_modified_date = Column(String, nullable=True)

    def __init__(self, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Pred({self.game + self.user})>"


