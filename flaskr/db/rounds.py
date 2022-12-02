from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from flaskr.db.base_model import Model


class Rounds(Model):
    """Predictions"""
    __tablename__ = 'tbl_rounds'
    id = Column(Integer, primary_key=True)
    round_name = Column(String, nullable=False)
    round_start_datetime = Column(String, nullable=False)
    round_start_timestamp = Column(Integer, nullable=False)
    round_end_datetime = Column(String, nullable=False)
    round_end_timestamp = Column(Integer, nullable=False)
    games = relationship("Games")

    def __init__(self, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)



