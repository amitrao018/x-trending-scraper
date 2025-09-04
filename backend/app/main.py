from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import database, models, schemas, crud, scraper

app = FastAPI(title="X Trends Scraper API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency for DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create tables on startup
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=database.engine)

# 🚀 Run scraper and save to DB
@app.post("/runs", response_model=schemas.TrendsRunOut)
def create_run(db: Session = Depends(get_db)):
    scraped_data = scraper.run_scraper()
    run_in = schemas.TrendsRunCreate(**scraped_data)
    created_run = crud.create_run(db, run_in)
    return created_run

# 📜 Get multiple runs
@app.get("/runs", response_model=List[schemas.TrendsRunOut])
def list_runs(limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_runs(db, limit)

# 🆕 Latest run only
@app.get("/latest", response_model=schemas.TrendsRunOut)
def get_latest_run(db: Session = Depends(get_db)):
    run = crud.get_runs(db, limit=1)
    if not run:
        return {"message": "No trends found, please run scraper first"}
    return run[0]

