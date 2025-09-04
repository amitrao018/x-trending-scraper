from sqlalchemy.orm import Session
from . import models, schemas
import uuid
import datetime

def create_run(db: Session, run: schemas.TrendsRunCreate):
    obj = models.TrendsRun(
        id=str(uuid.uuid4()),
        run_time=datetime.datetime.utcnow(),
        trend1=run.trend1,
        trend2=run.trend2,
        trend3=run.trend3,
        trend4=run.trend4,
        trend5=run.trend5,
        ip_address=run.ip_address,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get_runs(db: Session, limit: int = 20):
    return db.query(models.TrendsRun).order_by(models.TrendsRun.run_time.desc()).limit(limit).all()
