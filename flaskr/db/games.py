import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from flaskr.db.base_model import Model


class Games(Model):
    """Games"""

    __tablename__ = 'tbl_games'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    round_id = Column(Integer, ForeignKey('tbl_rounds.id'), index=True, default=1)
    team_a = Column(String, nullable=False)
    team_b = Column(String, nullable=False)
    score = Column(String, default=None)
    match_date = Column('match_date_timestamp', Integer, nullable=False)
    match_group = Column('match_group', String, nullable=False)
    predictions = relationship("Predictions")

    def __init__(self, **kwargs):
        """Create instance."""
        super().__init__(**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Games({self.team_a}; {self.team_b})>"
