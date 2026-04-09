import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uvicorn

# 1. Konfigurasi Database Neon.tech
# Ganti URL di bawah dengan Connection String asli Anda jika berbeda
DATABASE_URL = "postgresql://neondb_owner:npg_3xiZ7HFVMBTU@ep-lucky-wind-a14nbbr2-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Model Tabel Database
class NFTAsset(Base):
    __tablename__ = "nft_assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    image_url = Column(Text)

# Buat tabel otomatis
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Nusantara Engine V2")

# 3. Model Data untuk Input (Pydantic)
class AssetCreate(BaseModel):
    name: str
    description: str
    image_url: str

# 4. Endpoints
@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "Nusantara NFT Engine V2 Siap!",
        "database": "Terhubung ke Neon.tech"
    }

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
    return {"message": "Aset berhasil ditambahkan!", "data": new_asset}

# 5. Jalankan Server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)