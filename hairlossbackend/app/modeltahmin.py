from datetime import datetime
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from collections import Counter
from datetime import datetime

from app.photoAnalyze import sonuc_yorumla

veri = pd.read_csv('app/hair_loss_90k.csv', header=0)


def veri_kontrol(trained_models,test_verisi):
    analiz_parametreleri = [
    "proteinMiktari",
    "keratinMiktari",
    "sacDokusu",
    "vitaminMiktari",
    "manganezMiktari",
    "demirMiktari",
    "kalsiyumMiktari",
    "vucutSuMiktari",
    "stressSeviyesi",
    "karacigerDegeri"
    ]
    try:        
        test_verisi = [int(test_verisi.get(parametre)) for parametre in analiz_parametreleri if test_verisi.get(parametre) is not None]

        print("Analiz sonuçları:", test_verisi)
        
        x = AğırlıklıTahmin(trained_models,test_verisi)
              
        return SacDokulmesiTahmini(x)
    except Exception as hata:
        print(f"Hata oluştu: {hata}")



def AğırlıklıTahmin(trained_models, test_verisi):
    algoritmalar = trained_models['algoritmalar']
    performans_matrisi = trained_models['performans_matrisi']

    tahminler = []

    for isim, model in algoritmalar.items():
        try:
            if isinstance(test_verisi[0], list):
                tahmin = model.predict(test_verisi)[0]
            else:
                tahmin = model.predict([test_verisi])[0]

            tahmin = tahmin.item() if isinstance(tahmin, np.ndarray) else tahmin
            tahminler.append((isim, tahmin))

        except Exception as e:
            print(f"Model {isim} bir hata verdi: {e}")

    if not tahminler:
        print("\nHiçbir model tahmin üretemedi.")
        return None

    tahmin_sayilari = Counter([tahmin for _, tahmin in tahminler])
    en_cok_tekrar_tahmin, tekrar_sayisi = tahmin_sayilari.most_common(1)[0]
    print(f"\nEn çok tekrar eden tahmin: {en_cok_tekrar_tahmin} ({tekrar_sayisi} kez)")

    tahmin_agirlik_dict = {}
    for isim, tahmin in tahminler:
        model_agirlik = performans_matrisi.loc[isim, tahmin]

        if tahmin == en_cok_tekrar_tahmin:
            model_agirlik *= 0.5
        else:
            model_agirlik *= 0.5 / (len(tahminler) - tekrar_sayisi) 

        if tahmin not in tahmin_agirlik_dict:
            tahmin_agirlik_dict[tahmin] = 0
        tahmin_agirlik_dict[tahmin] += model_agirlik

    final_tahmin = max(tahmin_agirlik_dict.items(), key=lambda x: x[1])[0]
    print(f"\nAğırlıklı tahmin sonucu: {final_tahmin}")

    return final_tahmin


def SacDokulmesiTahmini(final_tahmin):
    level = round(final_tahmin)

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

    sonuc = tahminler.get(level, {
        "süre": "Bilinmiyor",
        "risk_seviyesi": "Belirlenemedi",
        "aciklama": "Geçersiz tahmin.",
        "genetik_risk": "Belirlenemedi",
        "tedavi_onerisi": "Uzman görüşü gerekli",
        "kontrol_siklik": "Belirlenemedi",
        "oneriler": ["Uzman görüşü alınmalı"],
        "risk_faktorleri": ["Belirlenemedi"]
    })

    print("\n=== Detaylı Saç Dökülmesi Analiz Raporu ===")
    print(f"\nTahmin Edilen Seviye: {level}")
    print(f"Risk Seviyesi: {sonuc['risk_seviyesi']}")
    print(f"Tahmini Süre: {sonuc['süre']}")
    print(f"Tedavi Önerisi: {sonuc['tedavi_onerisi']}")
    print(f"Kontrol Sıklığı: {sonuc['kontrol_siklik']}")
    print(f"\nAçıklama: {sonuc['aciklama']}")

    print("\nÖneriler:")
    for i, oneri in enumerate(sonuc['oneriler'], 1):
        print(f"{i}. {oneri}")

    print("\nRisk Faktörleri:")
    for i, risk in enumerate(sonuc['risk_faktorleri'], 1):
        print(f"{i}. {risk}")

    print("\nNot: Bu sonuçlar yapay zeka destekli tahminler içermektedir. Kesin teşhis ve tedavi için mutlaka bir uzmana başvurunuz.")

    return sonuc_yorumla(level)
