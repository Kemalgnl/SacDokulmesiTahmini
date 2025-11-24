import cv2
import os
import numpy as np
import pandas as pd
import urllib.request
import os
import cv2

def fotograflari_indir_ve_isle(yan_foto,arka_foto):
    try:
        yan_bytes = np.frombuffer(yan_foto.file.read(), np.uint8)
        arka_bytes = np.frombuffer(arka_foto.file.read(), np.uint8)

        yan_img = cv2.imdecode(yan_bytes, cv2.IMREAD_COLOR)
        arka_img = cv2.imdecode(arka_bytes, cv2.IMREAD_COLOR)

        if yan_img is None or arka_img is None:
            raise ValueError("Fotoğraflar çözümlenemedi (decode hatası).")

        print("Fotoğraflar RAM üzerinde çözümlendi.")


        arkadan_y = arkadan_fotograf_hesapla(arka_img)
        yandan_y = yandan_fotograf_hesapla(yan_img)

        ortalama = ortalama_yogunluk_hesapla(arkadan_y, yandan_y)
        grup = int(ortalama * 5)

        sonuc = sonuc_yorumla(grup)
        return sonuc

    except Exception as hata:
        return {"hata": str(hata)}

def yogunluk_hesapla(goruntu, yogunluk_degeri):
    gri = cv2.cvtColor(goruntu, cv2.COLOR_BGR2GRAY)
    _, ikili = cv2.threshold(gri, yogunluk_degeri, 255, cv2.THRESH_BINARY)
    return ikili

def piksel_deseni_olustur(goruntu, x1, x2, y1, y2):
    for i in range(x1, x2):
        for j in range(y1, y2):
            goruntu[j,i] = 255 if (i+j) % 2 == 0 else 0
    return goruntu

def sonuc_yorumla(deger):
    tahminler = {
    0: {"süre": "Belirtiler yok","risk_seviyesi": "Çok Düşük","aciklama": "Saç dökülmesi belirtisi görülmüyor.","tedavi_onerisi": "Koruyucu bakım yeterli","kontrol_siklik": "Yıllık kontrol","oneriler": [
        "Düzenli saç bakımı yapın","Sağlıklı beslenmeye devam edin","Stresten uzak durun","Yıllık saç analizi yaptırın"],
        "risk_faktorleri": ["Aşırı stres","Dengesiz beslenme","Sert kimyasallara maruz kalma"]},
    1: {"süre": "24 yıl","risk_seviyesi": "Düşük","aciklama": "Minimal düzeyde saç dökülmesi riski mevcut.","tedavi_onerisi": "Koruyucu bakım yeterli","kontrol_siklik": "Yıllık kontrol","oneriler": [
        "Düzenli saç bakımı yapın","Sağlıklı beslenmeye devam edin","Stresten uzak durun","Yıllık saç analizi yaptırın"],
        "risk_faktorleri": ["Aşırı stres","Dengesiz beslenme","Sert kimyasallara maruz kalma"]},
    2: {"süre": "18 yıl","risk_seviyesi": "Orta","aciklama": "Orta vadede saç dökülmesi riski bulunuyor.","tedavi_onerisi": "Koruyucu bakım yeterli","kontrol_siklik": "Yıllık kontrol","oneriler": [
        "Düzenli saç bakımı yapın","Sağlıklı beslenmeye devam edin","Stresten uzak durun","Yıllık saç analizi yaptırın"],
        "risk_faktorleri": ["Aşırı stres","Dengesiz beslenme","Sert kimyasallara maruz kalma"]},
    3: {"süre": "12 yıl","risk_seviyesi": "Yüksek","aciklama": "Belirgin saç dökülmesi riski tespit edildi.","tedavi_onerisi": "Koruyucu bakım yeterli","kontrol_siklik": "Yıllık kontrol","oneriler": [
        "Düzenli saç bakımı yapın","Sağlıklı beslenmeye devam edin","Stresten uzak durun","Yıllık saç analizi yaptırın"],
        "risk_faktorleri": ["Aşırı stres","Dengesiz beslenme","Sert kimyasallara maruz kalma"]},
    4: {"süre": "6 yıl","risk_seviyesi": "Çok Yüksek","aciklama": "Hızlı ilerleyen saç dökülmesi riski mevcut.","tedavi_onerisi": "Koruyucu bakım yeterli","kontrol_siklik": "Yıllık kontrol","oneriler": [
        "Düzenli saç bakımı yapın","Sağlıklı beslenmeye devam edin","Stresten uzak durun","Yıllık saç analizi yaptırın"],
        "risk_faktorleri": ["Aşırı stres","Dengesiz beslenme","Sert kimyasallara maruz kalma"]},
    5: {"süre": "Saç dökülmesi hali hazırda Mevcut","risk_seviyesi": "Kritik","aciklama": "Aktif saç dökülmesi mevcut.","tedavi_onerisi": "Koruyucu bakım yeterli","kontrol_siklik": "Yıllık kontrol","oneriler": [
        "Düzenli saç bakımı yapın","Sağlıklı beslenmeye devam edin","Stresten uzak durun","Yıllık saç analizi yaptırın"],
        "risk_faktorleri": ["Aşırı stres","Dengesiz beslenme","Sert kimyasallara maruz kalma"]}
    }
    sonuc = tahminler.get(deger, {
        "süre": "Hata Olustu Lütfen Tekrar Deneyin",
        "risk_seviyesi": "Hata Olustu Lütfen Tekrar Deneyin",
        "aciklama": "Hata Olustu Lütfen Tekrar Deneyin",
        "genetik_risk": "Hata Olustu Lütfen Tekrar Deneyin",
        "tedavi_onerisi": "Hata Olustu Lütfen Tekrar Deneyin",
        "kontrol_siklik": "Hata Olustu Lütfen Tekrar Deneyin",
        "oneriler": ["Hata Olustu Lütfen Tekrar Deneyin"],
        "risk_faktorleri": ["Hata Olustu Lütfen Tekrar Deneyin"]
    })
    return sonuc

def arkadan_fotograf_hesapla(self, goruntu):
    yogunluk = 100
    yuk, gen, _ = goruntu.shape
    kalinlik = 50

    self.piksel_deseni_olustur(goruntu, 0, gen, 0, kalinlik)
    self.piksel_deseni_olustur(goruntu, 0, gen, yuk - kalinlik, yuk)
    self.piksel_deseni_olustur(goruntu, 0, kalinlik, 0, yuk)
    self.piksel_deseni_olustur(goruntu, gen - kalinlik, gen, 0, yuk)

    islenmis = self.yogunluk_hesapla(goruntu, yogunluk)
    return np.mean(islenmis) / 255.0

def yandan_fotograf_hesapla(self, goruntu):
    yogunluk = 100
    yuk, gen = goruntu.shape[:2]

    for y in range(yuk):
        for x in range(gen):
            if y > (yuk/gen)*x:
                goruntu[y,x] = [255,255,255] if (x+y)%2==0 else [0,0,0]

    islenmis = self.yogunluk_hesapla(goruntu, yogunluk)
    return np.mean(islenmis) / 255.0

def ortalama_yogunluk_hesapla(self, a, b):
    return (a + b) / 2


