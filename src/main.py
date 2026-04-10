import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

# --- KONFIGURASI LOKASI FOLDER ---
# Karena main.py ada di dalam folder /src, kita perlu naik satu tingkat untuk cari folder /static
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# --- KONFIGURASI DATABASE NEON.TECH ---
DATABASE_URL = "postgresql://neondb_owner:npg_3xiZ7HFVMBTU@ep-lucky-wind-a14nbbr2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- MODEL TABEL ---
class NFTAsset(Base):
    __tablename__ = "nft_assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    image_url = Column(Text)

Base.metadata.create_all(bind=engine)

# --- APP SETUP ---
app = FastAPI(title="Nusantara Engine V2")

# Sambungkan folder static agar file CSS/JS/HTML bisa dibaca browser
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class AssetCreate(BaseModel):
    name: str
    description: str
    image_url: str

# --- ENDPOINTS ---

@app.get("/")
def serve_index():
    # Mengarahkan halaman utama langsung ke file index.html di folder static
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "File index.html tidak ditemukan di folder static"}

@app.get("/assets")
def get_assets():
    db = SessionLocal()
    assets = db.query(NFTAsset).all()
    db.close()
    return assets

@app.post("/assets")
def create_asset(asset: AssetCreate):
    db = SessionLocal()
    new_asset = NFTAsset(
        name=asset.name,
        description=asset.description,
        image_url=asset.image_url
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    db.close()
    return {"message": "Aset Berhasil Disimpan ke Neon.tech", "data": new_asset}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)


