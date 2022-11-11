import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean
from sqlalchemy.orm import relationship
from flaskr.db.base_model import Model


class Users(Model):
    """Users"""

    __tablename__ = 'tbl_users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    total_points = Column(Integer, default=None, nullable=True)
    is_admin = Column(Boolean, default=False)
    predictions = relationship("Predictions")

    def __init__(self, **kwargs):
        """Create instance."""
        super(Users, self).__init__(**kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return {'email': self.email}

    def __str__(self):
        """Represent instance as a unique string."""
        return {'email': self.email}


