from sqlalchemy import Column, String, DateTime
from .database import Base
import datetime
import uuid

def gen_uuid():
    return str(uuid.uuid4())

class TrendsRun(Base):
    __tablename__ = "trends_runs"
    id = Column(String(36), primary_key=True, index=True, default=gen_uuid)
    run_time = Column(DateTime, default=datetime.datetime.utcnow)
    trend1 = Column(String, nullable=True)
    trend2 = Column(String, nullable=True)
    trend3 = Column(String, nullable=True)
    trend4 = Column(String, nullable=True)
    trend5 = Column(String, nullable=True)
    ip_address = Column(String, nullable=True)
