import time
import datetime
import requests
import os
import uuid
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
X_USERNAME = os.getenv("X_USERNAME")
X_PASSWORD = os.getenv("X_PASSWORD")
DATABASE_URL = os.getenv("DATABASE_URL")

if not X_USERNAME or not X_PASSWORD:
    raise ValueError("X_USERNAME and X_PASSWORD must be set in .env")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL must be set in .env")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Run(Base):
    __tablename__ = "runs"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    trend1 = Column(String)
    trend2 = Column(String)
    trend3 = Column(String)
    trend4 = Column(String)
    trend5 = Column(String)
    ip_address = Column(String)
    run_time = Column(DateTime, default=datetime.datetime.utcnow)

Base.metadata.create_all(bind=engine)


def run_scraper():

    options = Options()
    #  Disable headless for debugging
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:

        driver.get("https://x.com/login")
        time.sleep(3)


        username_field = driver.find_element(By.NAME, "text")
        username_field.send_keys(X_USERNAME)
        driver.find_element(By.XPATH, '//span[text()="Next"]').click()
        time.sleep(2)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(X_PASSWORD)
        driver.find_element(By.XPATH, '//span[text()="Log in"]').click()
        time.sleep(7)


        driver.get("https://x.com/home")
        time.sleep(7)


        driver.save_screenshot("homepage.png")
        print("📸 Screenshot saved as homepage.png")

        # Dump first 50 span texts (for debugging)
        all_texts = [el.text for el in driver.find_elements(By.XPATH, "//span") if el.text.strip()]
        print("📝 Dump of first 50 <span> texts:")
        for t in all_texts[:50]:
            print("-", t)


        elements = driver.find_elements(
            By.XPATH, "//section[@aria-label='Timeline: Trending now']//span"
        )
        trends = [el.text.strip() for el in elements if el.text.strip()]

        if not trends:
            elements = driver.find_elements(
                By.XPATH, "//section[contains(., \"What’s happening\")]//span"
            )
            trends = [el.text.strip() for el in elements if el.text.strip()]

        clean_trends = []
        for t in trends:
            if any(x in t.lower() for x in ["what’s happening", "trending", "posts", "for you"]):
                continue
            if len(t) < 2:
                continue
            clean_trends.append(t)

        clean_trends = list(dict.fromkeys(clean_trends))
        print("🔎 Extracted trends (cleaned):", clean_trends)

        top5 = clean_trends[:5]

        # Get IP
        ip = requests.get("https://api64.ipify.org?format=json").json()["ip"]

        result = {
            "run_time": datetime.datetime.utcnow().isoformat() + "Z",
            "trend1": top5[0] if len(top5) > 0 else None,
            "trend2": top5[1] if len(top5) > 1 else None,
            "trend3": top5[2] if len(top5) > 2 else None,
            "trend4": top5[3] if len(top5) > 3 else None,
            "trend5": top5[4] if len(top5) > 4 else None,
            "ip_address": ip
        }


        db = SessionLocal()
        db_run = Run(
            trend1=result["trend1"],
            trend2=result["trend2"],
            trend3=result["trend3"],
            trend4=result["trend4"],
            trend5=result["trend5"],
            ip_address=result["ip_address"],
            run_time=datetime.datetime.utcnow()
        )
        db.add(db_run)
        db.commit()
        db.refresh(db_run)
        db.close()

        print("\n📌 Final JSON:\n", result)
        print("✅ Saved to Postgres (runs table).")

        return result

    finally:
        driver.quit()


if __name__ == "__main__":
    run_scraper()






