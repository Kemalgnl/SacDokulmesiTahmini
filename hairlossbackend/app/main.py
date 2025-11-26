from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile,Body
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime

from app.model_eğitim1 import model_Train
from app.modeltahmin import veri_kontrol
from app.photoAnalyze import fotograflari_indir_ve_isle
#from app.model_eğitim1 import trained_models, performans_matrisi

#backend .\venv\Scripts\Activate  python -m uvicorn app.main:app --reload
#frontend npm start
load_dotenv()

app = FastAPI(
    title="Hairloss Backend",
    description="FastAPI sunucusunun temel yapısı."
)
origins = [
    "https://kgdevhairloss.netlify.app/",
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def train_Data():
    global trained_models
    print("Uygulama başlıyor model_Train hazırlanıyor")
    trained_models = model_Train()
    print("model_Train hazır")


@app.post("/MakeDataAnalayze")
def make_DataAnalayze(test_verisi: dict = Body(...)):
    sonuc = veri_kontrol(trained_models, test_verisi)
    return {"sonuc": sonuc}

@app.post("/MakePhotoAnalayze")
def make_PhotoAnalayze(YandanPhoto: UploadFile = File(...),ArkadanPhoto: UploadFile = File(...),):
    response=fotograflari_indir_ve_isle(YandanPhoto,ArkadanPhoto)
    
    return {"sonuc": response}

async def restart_server():
    url = "https://sacdokulmesitahmini-8.onrender.com/" 
    while True:
        try:
            async with httpx.AsyncClient() as istemci:
                await istemci.get(url)
                print("Ping gönderildi!")
        except Exception as hata:
            print("Ping başarısız:", hata)
        await asyncio.sleep(50) 

@app.on_event("startup")
async def uygulama_baslangici():
    asyncio.create_task(restart_server())
    print("Uygulama başlatıldı, ping döngüsü çalışıyor...")


