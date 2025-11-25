import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier, OneVsOneClassifier

import seaborn as sns
import matplotlib.pyplot as plt
import random


rf_model = None
logreg_model = None
knn_model = None
xgb_model = None
ann_model = None
lgbm_model = None
catboost_model = None
benim_modelim = None
lgbm_model_ova = None
catboost_model_ova = None
lgbm_model_ovo = None
catboost_model_ovo = None

performans_matrisi = None
train_data = None

# -----------------------------------------sayısal analiz model eğitimi ----------
def model_Train():
    global trained_models
    global rf_model, logreg_model, knn_model, xgb_model, ann_model, lgbm_model, catboost_model, benim_modelim
    global lgbm_model_ova,catboost_model_ova, lgbm_model_ovo, catboost_model_ovo, performans_matrisi, train_data

    veri = pd.read_csv('hairlossbackend/app//hair_loss_90k.csv', header=0)
    class BenimModelim:
        def __init__(self):
            self.katsayilar = None

        def fit(self, X, y):
            X_matrisi = np.array(X)
            Y_vektor = np.array(y)

            x_transpozu = X_matrisi.T
            x_transpoz_x = x_transpozu @ X_matrisi
            ters_x_transpoz_x = np.linalg.inv(x_transpoz_x)

            x_transpoz_y = x_transpozu @ Y_vektor
            self.katsayilar = ters_x_transpoz_x @ x_transpoz_y

            return self

        def predict(self, X):
            X = np.array(X, dtype=float)

            if len(X.shape) == 1:
                X = X.reshape(1, -1)

            tahminler = []
            for x in X:
                SonTahmin = np.sum(self.katsayilar * x)
                SonTahmin *= 10

                tam_kisim = int(SonTahmin)
                ondalik_kisim = SonTahmin - tam_kisim

                if ondalik_kisim >= 0.5:
                    tam_kisim += 1

                tahminler.append(max(0, min(5, tam_kisim)))

            return np.array(tahminler)



    X = veri.drop(columns=["hair_fall"])
    y = veri["hair_fall"]

    ss = StandardScaler()
    X_test = ss.transform(X)


    X_egitim, X_test, y_egitim, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    svm_model = SVC(kernel="rbf", random_state=42, probability=True)
    logreg_model = LogisticRegression(random_state=42)
    knn_model = KNeighborsClassifier(n_neighbors=5)
    xgb_model = XGBClassifier(n_estimators=100, random_state=42, learning_rate=0.05)
    ann_model = MLPClassifier(hidden_layer_sizes=(50, 50), max_iter=1000, random_state=42)
    lgbm_model = LGBMClassifier(n_estimators=100, random_state=42, learning_rate=0.1)
    catboost_model = CatBoostClassifier(iterations=100, random_state=42, verbose=0)
    benim_modelim = BenimModelim()

    rf_model.fit(X_egitim, y_egitim)
    svm_model.fit(X_egitim, y_egitim)
    logreg_model.fit(X_egitim, y_egitim)
    knn_model.fit(X_egitim, y_egitim)
    xgb_model.fit(X_egitim, y_egitim)
    ann_model.fit(X_egitim, y_egitim)
    lgbm_model.fit(X_egitim, y_egitim)
    catboost_model.fit(X_egitim, y_egitim)
    benim_modelim.fit(X_egitim, y_egitim)

    rf_accuracy = accuracy_score(y_test, rf_model.predict(X_test))
    svm_accuracy = accuracy_score(y_test, svm_model.predict(X_test))
    logreg_accuracy = accuracy_score(y_test, logreg_model.predict(X_test))
    knn_accuracy = accuracy_score(y_test, knn_model.predict(X_test))
    xgb_accuracy = accuracy_score(y_test, xgb_model.predict(X_test))
    ann_accuracy = accuracy_score(y_test, ann_model.predict(X_test))
    lgbm_accuracy = accuracy_score(y_test, lgbm_model.predict(X_test))
    catboost_accuracy = accuracy_score(y_test, catboost_model.predict(X_test))
    benim_modelim_accuracy = accuracy_score(y_test, benim_modelim.predict(X_test))

    results = {}

    # LightGBM - OvA
    lgbm_model_ova = OneVsRestClassifier(
        LGBMClassifier(n_estimators=100, max_depth=10, learning_rate=0.1, random_state=42)
    )
    lgbm_model_ova.fit(X_egitim, y_egitim)
    lgbm_preds_ova = lgbm_model_ova.predict(X_test)
    results["LightGBM (OvA)"] = accuracy_score(y_test, lgbm_preds_ova)

    catboost_model_ova = OneVsRestClassifier(
        CatBoostClassifier(
            iterations=100, depth=10, learning_rate=0.1, random_state=42, verbose=0
        )
    )
    catboost_model_ova.fit(X_egitim, y_egitim)
    catboost_preds_ova = catboost_model_ova.predict(X_test)
    results["CatBoost (OvA)"] = accuracy_score(y_test, catboost_preds_ova)

    # OvO modelleri
    lgbm_model_ovo = OneVsOneClassifier(
        LGBMClassifier(n_estimators=100, max_depth=10, learning_rate=0.1, random_state=42)
    )
    lgbm_model_ovo.fit(X_egitim, y_egitim)
    lgbm_preds_ovo = lgbm_model_ovo.predict(X_test)
    results["LightGBM (OvO)"] = accuracy_score(y_test, lgbm_preds_ovo)

    catboost_model_ovo = OneVsOneClassifier(
        CatBoostClassifier(
            iterations=100, depth=10, learning_rate=0.1, random_state=42, verbose=0
        )
    )
    catboost_model_ovo.fit(X_egitim, y_egitim)
    catboost_preds_ovo = catboost_model_ovo.predict(X_test)
    results["CatBoost (OvO)"] = accuracy_score(y_test, catboost_preds_ovo)


    print(f"RF Modeli Doğruluğu: {rf_accuracy:.4f}")
    print(f"SVM Modeli Doğruluğu: {svm_accuracy:.4f}")
    print(f"Logistic Regression Modeli Doğruluğu: {logreg_accuracy:.4f}")
    print(f"KNN Modeli Doğruluğu: {knn_accuracy:.4f}")
    print(f"XGB Modeli Doğruluğu: {xgb_accuracy:.4f}")
    print(f"ANN Modeli Doğruluğu: {ann_accuracy:.4f}")
    print(f"LGBM Modeli Doğruluğu: {lgbm_accuracy:.4f}")
    print(f"CatBoost Modeli Doğruluğu: {catboost_accuracy:.4f}")
    print(f"Benim Modelim Doğruluğu: {benim_modelim_accuracy:.4f}")

   
    egitim_verisi = []#hairloss 10k
    label_sayilari = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    hedef_sayi = 50
    arama_sayisi = 0
    max_arama = 500

    while min(label_sayilari.values()) < hedef_sayi and arama_sayisi < max_arama:
        index = random.randint(0, len(veri)-1)
        row = veri.iloc[index]

        features = row[:10].tolist()
        label = int(row[10])

        if label_sayilari[label] < hedef_sayi:
            ornek = {
                "features": features,
                "label": label
            }
            egitim_verisi.append(ornek)
            label_sayilari[label] += 1
            print(f"Label {label} için {label_sayilari[label]}. örnek eklendi")
            print(f"features: {ornek['features']}, label: {ornek['label']}")

        arama_sayisi += 1


    algoritmalar = {
        "Random Forest": rf_model,
        "Logistic Regression": logreg_model,
        "KNN": knn_model,
        "XGB": xgb_model,
        "ANN": ann_model,
        "LightGBM": lgbm_model,
        "Benim Modelim": benim_modelim,
        "CatBoost": catboost_model,
        "LightGBM (OvA)": lgbm_model_ova,
        "CatBoost (OvA)": catboost_model_ova,
        "LightGBM (OvO)": lgbm_model_ovo,
        "CatBoost (OvO)": catboost_model_ovo

    }
    ModelPerformansMatrisi(algoritmalar, egitim_verisi)

    return {
        "algoritmalar": algoritmalar,
        "performans_matrisi": performans_matrisi
    }

 
def ModelPerformansMatrisi(algoritmalar, egitim_verisi):
    X = np.array([veri["features"] for veri in egitim_verisi])
    y = np.array([veri["label"] for veri in egitim_verisi])

    performans_matrisi = pd.DataFrame(index=algoritmalar.keys(), columns=sorted(set(y)))

    for model_adi, model in algoritmalar.items():
        try:
            tahminler = model.predict(X)
            for sinif in sorted(set(y)):

                dogruluk = accuracy_score([1 if label == sinif else 0 for label in y],
                                          [1 if tahmin == sinif else 0 for tahmin in tahminler])
                performans_matrisi.loc[model_adi, sinif] = dogruluk
        except Exception as e:
            print(f"{model_adi} için hata: {e}")
            performans_matrisi.loc[model_adi] = None

    plt.figure(figsize=(8, 5))
    sns.heatmap(performans_matrisi.astype(float), annot=True, cmap='YlOrRd', fmt='.2f')
    plt.title('Model Performans Matrisi')
    plt.xlabel('Saç Dökülme Seviyesi')
    plt.ylabel('Model')
    plt.show()

    en_iyi_modeller = {}
    for sinif in sorted(set(y)):
        en_iyi_model = performans_matrisi[sinif].idxmax()
        en_iyi_skor = performans_matrisi[sinif].max()
        en_iyi_modeller[sinif] = (en_iyi_model, en_iyi_skor)
        print(f"\nSeviye {sinif} için en iyi model: {en_iyi_model} (Doğruluk: {en_iyi_skor:.2f})")

    return performans_matrisi, en_iyi_modeller

