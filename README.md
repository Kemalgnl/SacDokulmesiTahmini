# Hair Loss Detection and Tracking System

Saç dökülmesini görüntü işleme ve makine öğrenmesi yöntemleri ile analiz etmek amacıyla geliştirilmiş bir takip sistemidir.  
Kullanıcıdan alınan saç/scalp görüntüleri üzerinden analiz yapılarak saç yoğunluğu, dökülme seviyesi ve zaman içerisindeki değişim takip edilmektedir.

Bu proje bitirme projesi kapsamında geliştirilmiştir.

---

## Kullanılan Teknolojiler

### Backend
- Python
- Flask / FastAPI

### Frontend
- React.js

### Yapay Zekâ & Görüntü İşleme
- TensorFlow
- Keras
- OpenCV
- Scikit-learn
- NumPy
- Pandas

### Veritabanı
- SQLite / MongoDB

---

## Proje Özellikleri

- Saç dökülmesi tespiti
- Saç yoğunluğu analizi
- Zamana bağlı değişim takibi
- Çoklu model kullanımı
- Ensemble tahmin sistemi
- Görüntü ön işleme
- Model performans karşılaştırması
- Geçmiş analiz kayıtları

---

## Kullanılan Modeller

Projede farklı makine öğrenmesi modelleri birlikte kullanılmıştır.

- CNN
- MobileNet
- ResNet
- Random Forest
- SVM

Farklı modellerin çıktıları birleştirilerek daha stabil sonuçlar elde edilmiştir.

---

## Ensemble Yapısı

Tahmin sonuçları aşağıdaki yöntemlerle birleştirilmiştir:

- Majority Voting
- Weighted Prediction

Bu yapı sayesinde:
- Tek modele bağlı hata oranı azaltılmıştır
- Genel doğruluk oranı artırılmıştır
- Daha güvenilir sonuçlar elde edilmiştir

---

## Sistem Akışı

```text
Görüntü Alma
    ↓
Ön İşleme
    ↓
Öznitelik Çıkarma
    ↓
Makine Öğrenmesi Modelleri
    ↓
Ensemble Tahmin
    ↓
Sonuç ve Takip
```

---

## Kullanım

1. Sisteme giriş yapılır
2. Saç görüntüsü yüklenir
3. Analiz başlatılır
4. Model sonuçları görüntülenir
5. Önceki analizlerle karşılaştırma yapılabilir

---

## Model Sonuçları

| Model | Accuracy |
|---|---|
| CNN | 92% |
| MobileNet | 90% |
| ResNet | 94% |
| Random Forest | 87% |
| SVM | 85% |

> Sonuçlar kullanılan veri setine göre değişiklik gösterebilir.

---

## Gelecek Çalışmalar

- Mobil uygulama desteği
- Gerçek zamanlı analiz
- Daha büyük veri setleri ile eğitim
- Bulut tabanlı analiz sistemi
- Dermatoloji destek entegrasyonu

---

## Lisans

Bu proje eğitim ve araştırma amaçlı geliştirilmiştir.

---
