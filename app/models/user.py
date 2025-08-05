from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True)

    role = relationship("Role")
    team = relationship("Team")
    company = relationship("Company")
