from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

# --- 1. KONFIGURASI DATABASE ---
DATABASE_URL = "postgresql://neondb_owner:npg_3xiZ7HFVMBTU@ep-lucky-wind-a14nbbr2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

Base = declarative_base()
class NusantaraNFT(Base):
    _tablename_ = "nusantara_nfts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    category = Column(String(50))
    creator_wallet = Column(String(100))

engine = create_engine("postgresql://neondb_owner:npg_3xiZ7HFVMBTU@ep-lucky-wind-a14nbbr2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    db = SessionLocal()
    nfts = db.query(NusantaraNFT).all()
    db.close()
    return templates.TemplateResponse("index.html", {"request": request, "nfts": nfts})

@app.post("/add-nft")
async def add_nft(name: str = Form(...), category: str = Form(...), creator_wallet: str = Form(...)):
    db = SessionLocal()
    try:
        new_nft = NusantaraNFT(name=name, category=category, creator_wallet=creator_wallet)
        db.add(new_nft)
        db.commit()
        return RedirectResponse(url="/", status_code=303)
    finally:
        db.close()

@app.get("/admin-icp2e", response_class=HTMLResponse)
async def admin_panel(request: Request):
    db = SessionLocal()
    count = db.query(NusantaraNFT).count()
    db.close()
    return templates.TemplateResponse("admin.html", {"request": request, "total": count})

if _name_ == "_main_":
    uvicorn.run(app, host="0.0.0.0", port=5000)
