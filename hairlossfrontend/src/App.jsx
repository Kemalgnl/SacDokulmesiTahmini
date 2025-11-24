import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";
import { FaCamera, FaFileAlt, FaHome,FaLinkedin,FaGithubSquare   } from "react-icons/fa";
import { IoAnalytics } from "react-icons/io5";
import { CgProfile } from "react-icons/cg";

import { send_Data, send_Photo } from "./api.js";

function App() {
  const [activePage, setActivePage] = useState("home");
  const [localState, setLocalState] = useState([]);

  const [inputProteinMiktari, setInputProteinMiktari] = useState("");
  const [inputKeratinMiktari, setInputKeratinMiktari] = useState("");
  const [inputSacDokusu, setInputSacDokusu] = useState("");
  const [inputVitaminMiktari, setInputVitaminMiktari] = useState("");
  const [inputManganezMiktari, setInputManganezMiktari] = useState("");
  const [inputDemirMiktari, setInputDemirMiktari] = useState("");
  const [inputKalsiyumMiktari, setInputKalsiyumMiktari] = useState("");
  const [inputVucutSuMiktari, setInputVucutSuMiktari] = useState("");
  const [inputStressSeviyesi, setInputStressSeviyesi] = useState("");
  const [inputKaracigerDegeri, setInputKaracigerDegeri] = useState("");

  const handleProteinChange = (event) =>
    setInputProteinMiktari(event.target.value);
  const handleKeratinChange = (event) =>
    setInputKeratinMiktari(event.target.value);
  const handleSacDokusuChange = (event) =>
    setInputSacDokusu(event.target.value);
  const handleVitaminChange = (event) =>
    setInputVitaminMiktari(event.target.value);
  const handleManganezChange = (event) =>
    setInputManganezMiktari(event.target.value);
  const handleDemirChange = (event) => setInputDemirMiktari(event.target.value);
  const handleKalsiyumChange = (event) =>
    setInputKalsiyumMiktari(event.target.value);
  const handleVucutSuChange = (event) =>
    setInputVucutSuMiktari(event.target.value);
  const handleStressChange = (event) =>
    setInputStressSeviyesi(event.target.value);
  const handleKaracigerChange = (event) =>
    setInputKaracigerDegeri(event.target.value);

  const [responseId, setresponseId] = useState(1);

  async function send_data() {
    let response;
    const test_verisi = {
      proteinMiktari: inputProteinMiktari,
      keratinMiktari: inputKeratinMiktari,
      sacDokusu: inputSacDokusu,
      vitaminMiktari: inputVitaminMiktari,
      manganezMiktari: inputManganezMiktari,
      demirMiktari: inputDemirMiktari,
      kalsiyumMiktari: inputKalsiyumMiktari,
      vucutSuMiktari: inputVucutSuMiktari,
      stressSeviyesi: inputStressSeviyesi,
      karacigerDegeri: inputKaracigerDegeri,
    };

    console.log("send data çağırıldı");
    console.log(test_verisi);

    if (test_verisi == null) return;

    response = await send_Data(test_verisi);
    console.log(response);

    const newEntry = {
      id: responseId + 1,
      sonuc: response.sonuc,
    };
    setActivePage("home");
    setresponseId((prevId) => prevId + 1);

    setLocalState((prev) => [...prev, newEntry]);
  }

  async function send_photo() {
    console.log("send photo çağırıldı");
    let response;
    const formData = new FormData();
    
    const YandanPhoto = document.querySelector(
      'input[name="cameraYandanPhoto"]'
    ).files[0];
    const ArkadanPhoto = document.querySelector(
      'input[name="cameraArkadanPhoto"]'
    ).files[0];

    if (YandanPhoto) formData.append("YandanPhoto", YandanPhoto);
    if (ArkadanPhoto) formData.append("ArkadanPhoto", ArkadanPhoto);

    if (!YandanPhoto && !ArkadanPhoto) return;

    response = await send_Photo(YandanPhoto, ArkadanPhoto);
    
    console.log(response);
    
    setActivePage("home");
    const newEntry = {
      id: responseId + 1, 
      sonuc: response.sonuc,
    };

    setresponseId((prevId) => prevId + 1);

    setLocalState((prev) => [...prev, newEntry]);
  }

  async function open_result() {
    setActivePage("result");
  }
  async function clickedAnalayzePage() {
    setActivePage("analyze");
  }
  async function clickedHomePage() {
    setActivePage("home");
  }
  async function clickedProfilePage() {
    setActivePage("profile");
  }
  async function clickedCameraIcon() {
    setActivePage("camera");
  }
  async function clickedDataIcon() {
    setActivePage("numeric");
  }
  const renderScreen = () => {
    switch (activePage) {
      case "home":
        return (
          <>
            <div className="headerOne"></div>
            <div className="headerTwo">
              <h2>Saç Dökülmesi Analizi</h2>
            </div>

            <div className="textSendhairData">
              <h1>Saç Bilgilerinizi gönderin</h1>
            </div>

            <div className="dataUploadContainer">
              <div
                onClick={clickedCameraIcon}
                className="uploadPhotoContainer iconContainer"
              >
                <FaCamera className="icon" />
                Fotograf yükleyin
              </div>
              <div
                onClick={clickedDataIcon}
                className="uploadNumericContainer iconContainer"
              >
                <FaFileAlt className="icon" />
                Sayısal veri yükleyin
              </div>
            </div>

            <div className="textanalyze">
              <h1>Analiz Geçmişi</h1>
            </div>

            <div className="historyResult">
              {localState.map((item) => (
                <div
                  onClick={() => open_result(item)}
                  key={item.id}
                  className="level"
                >
                  <p>
                    <strong>Sonuç {item.id}</strong>
                  </p>
                  <p>
                    Saç dökülmesi:{" "}
                    {item.sonuc.seviye
                      ? item.sonuc.seviye + ". seviye"
                      : "Bilinmiyor"}
                  </p>
                  <p>Kontrol: {item.sonuc.kontrol_siklik || "Bilinmiyor"}</p>
                  <p>
                    Risk seviyesi: {item.sonuc.risk_seviyesi || "Bilinmiyor"}
                  </p>
                </div>
              ))}
            </div>
          </>
        );
      case "camera":
        return (
          <div className="cameraFormContainer">
            <div className="cameraCard">
              <h3 className="cameraTitle">Saç Fotoğraf Yükleme</h3>

              <div className="cameraInputs">
                <div className="cameraInputGroup">
                  <label>Yandan Fotoğraf Seçin:</label>
                  <input
                    type="file"
                    name="cameraYandanPhoto"
                    accept="image/*"
                    capture="environment"
                  />
                </div>

                <div className="cameraInputGroup">
                  <label>Arkadan Fotoğraf Seçin:</label>
                  <input
                    type="file"
                    name="cameraArkadanPhoto"
                    accept="image/*"
                    capture="environment"
                  />
                </div>

                <div className="cameraSubmitButton">
                  <button onClick={send_photo}>GÖNDER</button>
                </div>
              </div>
            </div>
          </div>
        );

      case "numeric":
        return (
          <div className="dataFormContainer">
            <div className="analysisCard">
              <h3 className="analysisTitle">Saç Analizi Formu</h3>
              <div className="analysisInputs">
                <div className="inputGroup">
                  <label>Protein Miktarı (1-500):</label>
                  <input
                    type="number"
                    value={inputProteinMiktari}
                    onChange={handleProteinChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Keratin Miktarı (1-500):</label>
                  <input
                    type="number"
                    value={inputKeratinMiktari}
                    onChange={handleKeratinChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Saç Dokusu (1-500):</label>
                  <input
                    type="number"
                    value={inputSacDokusu}
                    onChange={handleSacDokusuChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Vitamin Miktarı (1-500):</label>
                  <input
                    type="number"
                    value={inputVitaminMiktari}
                    onChange={handleVitaminChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Manganez Miktarı (1-500):</label>
                  <input
                    type="number"
                    value={inputManganezMiktari}
                    onChange={handleManganezChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Demir Miktarı (1-500):</label>
                  <input
                    type="number"
                    value={inputDemirMiktari}
                    onChange={handleDemirChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Kalsiyum Miktarı (1-500):</label>
                  <input
                    type="number"
                    value={inputKalsiyumMiktari}
                    onChange={handleKalsiyumChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Vücut Su Miktarı (1-500):</label>
                  <input
                    type="number"
                    value={inputVucutSuMiktari}
                    onChange={handleVucutSuChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Stres Seviyesi (1-500):</label>
                  <input
                    type="number"
                    value={inputStressSeviyesi}
                    onChange={handleStressChange}
                    min="1"
                    max="500"
                  />
                </div>

                <div className="inputGroup">
                  <label>Karaciğer Değeri (1-500):</label>
                  <input
                    type="number"
                    value={inputKaracigerDegeri}
                    onChange={handleKaracigerChange}
                    min="1"
                    max="500"
                  />
                </div>
                <div className="submitButton">
                  <button onClick={send_data}>GÖNDER</button>
                </div>
              </div>
            </div>
          </div>
        );

      case "result":
        return (
          <div className="showResult">
            {localState.map((item) => (
              <div
                onClick={() => open_result(item)}
                key={item.id}
                className="results"
              >
                <div className="resultCard">
                  <p className="resultTitle">
                    <strong>ANALİZ DETAYLARI {item.id}</strong>
                  </p>

                  <div className="resultInfo">
                    <p>
                      <strong>Saç dökülmesi:</strong>{" "}
                      {item.sonuc.seviye
                        ? item.sonuc.seviye + ". seviye"
                        : "Bilinmiyor"}
                    </p>
                    <p>
                      <strong>Kontrol:</strong>{" "}
                      {item.sonuc.kontrol_siklik || "Bilinmiyor"}
                    </p>
                    <p>
                      <strong>Risk seviyesi:</strong>{" "}
                      {item.sonuc.risk_seviyesi || "Bilinmiyor"}
                    </p>
                  </div>

                  <div className="suggestions">
                    <h4>Öneriler</h4>
                    <ul>
                      {item.sonuc.oneriler?.map((oneri, idx) => (
                        <li key={idx}>{oneri}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="riskFactors">
                    <h4>Risk Faktörleri</h4>
                    <ul>
                      {item.sonuc.risk_faktorleri?.map((risk, idx) => (
                        <li key={idx}>{risk}</li>
                      ))}
                    </ul>
                  </div>

                  <div className="levelInfo">
                    <p>
                      <strong>Risk Seviyesi:</strong>{" "}
                      {item.sonuc.risk_seviyesi || "Bilinmiyor"}
                    </p>
                    <p>
                      <strong>Seviye:</strong>{" "}
                      {item.sonuc.seviye || "Bilinmiyor"}
                    </p>
                    <p>
                      <strong>Tahmini Süre:</strong>{" "}
                      {item.sonuc.tahmini_sure || "Bilinmiyor"}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        );

      case "analyze":
        return (
          <div className="analyzePage">
            <div className="headerOne"></div>
            <div className="headerTwo">
              <p>Saç Dökülmesi Analizi</p>
            </div>

            <div className="percentageContainer">
              <div className="percentage">
                <h2>%65</h2>
              </div>
              <div className="ratio">YÜKSEK-ORTA RİSK</div>
              <div className="info">
                <div className="analyzeRow">
                  <div className="hairDensity">
                    <p className="p1">7,8</p>
                    <p>Saç Yoğunluğu</p>
                  </div>
                  <div className="modelsecurity">
                    <p className="p1">%82</p>
                    <p>Model Güveni</p>
                  </div>
                </div>
                <div className="analayzeColumn">
                  <div className="healtScore">
                    <p className="p1">6,2</p>
                    <p>Saglık Skoru</p>
                  </div>
                  <div className="cotrolPeriod">
                    <p className="p1">1 AY</p>
                    <p>Tarama Periyodu</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="analyzehistoryResult">
              <div className="sugges 1">
                <p>
                  Vitamin Desteği: Biotin, Vitamin D ve Demir takviyeleri
                  kullanımı önerilir.{" "}
                </p>
              </div>
              <div className="sugges 2">
                <p>
                  Stres Yönetimi: Günlük 15 dakika meditasyon veya yoga yapın.
                </p>
              </div>
              <div className="sugges 3">
                <p>
                  Beslenme: Protein açısından zengin gıdalar tüketin (yumurta,
                  balık, kuruyemiş).
                </p>
              </div>
              <div className="sugges 4">
                <p>
                  Uzman Görüşü: 3 ay içinde dermatoloji uzmanına kontrole gidin.
                </p>
              </div>
            </div>
          </div>
        );

      case "profile":
        return (
          <div className="profilePage">
            <div className="headerOne"></div>
            <div className="headerTwo">
              <p>Saç Dökülmesi Analizi</p>
            </div>
            <div className="profilePageContainer">
              <div className="profilePhoto">
                <img src="./images/human.jpg" alt="" />
              </div>
              <div className="name">
                <p>Ahmet Yılmaz</p>
              </div>
              <div className="totalAnalyze">
                <p className="p1">15</p>
                <p>Toplam Analiz</p>
              </div>
              <div className="recovery">
                <p className="p1">%85</p>
                <p>İyileşme</p>
              </div>
            </div>
            <div className="profileInfo">
              <div className="profileinfos">
                <p>Kişisel Bilgiler</p>
              </div>
              <div className="profileAge">
                <p>Yaş</p>
                <p className="age">25</p>
              </div>
              <div className="profileGender">
                <p>Cinsiyet</p>
                <p className="gender">Erkek</p>
              </div>
              <div className="registerDate">
                <p>Üyelik Tarihi</p>
                <p className="date">25.10.2025</p>
              </div>
              <div className="lastAnalayze">
                <p>Son Analiz</p>
                <p className="last">25.10.2025</p>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="main">
      <div class="leftContainer">
        <h2>Nasıl Çalışır?</h2>
        <p>
          <strong>Fotoğraf Yükleyin:</strong> Uygulama, kullanıcıların saç
          fotoğraflarını analiz ederek dökülme seviyesini belirler. Yandan veya
          arkadan çekilen fotoğraflar, yoğunluk analizi yapılarak dökülme oranı
          hesaplanır.
        </p>

        <p>
          <strong>Sayısal Veriler Yükleyin:</strong> Beslenme, yaş ve cinsiyet
          gibi biyokimyasal parametreler, saç dökülmesi riski hakkında daha
          fazla bilgi sağlar. Bu veriler, kullanıcıların kişisel durumlarına
          göre analiz edilir.
        </p>

        <h2>Sonuçlar ve Risk Seviyeleri</h2>

        <div className="section-title">
          Uygulama, kullanıcıların saç dökülmesi seviyesini 5 farklı risk
          kategorisinde değerlendirir:
        </div>

        <div className="risk-list">
          <ul>
            <li className="risk-item">
              Çok Düşük Risk: Yıllık kontrol, temel öneriler
            </li>
            <li className="risk-item">
              Düşük Risk: 6 aylık kontrol, temel beslenme önerileri
            </li>
            <li className="risk-item">
              Orta Düşük Risk: 4 aylık kontrol, vitamin önerileri
            </li>
            <li className="risk-item">
              Orta Yüksek Risk: 3 aylık kontrol, stres yönetimi
            </li>
            <li className="risk-item">
              Yüksek Risk: 2 aylık kontrol, dermatolog önerisi
            </li>
            <li className="risk-item">
              Çok Yüksek Risk: Aylık kontrol, acil uzman görüşü
            </li>
          </ul>
        </div>
        <div className="social-buttons">
          <a
            href="https://www.linkedin.com/in/kemalginali/"
            target="_blank"
            className="social-button linkedin"
          >
            <FaLinkedin className="leftcontainerIcons"/> LinkedIn
          </a>
          <a
            href="https://github.com/Kemalgnl"
            target="_blank"
            className="social-button github"
          >
            <FaGithubSquare className="leftcontainerIcons"/> GitHub
            
          </a>
          <a
            href="https://kgdevportfolio.netlify.app/"
            target="_blank"
            className="social-button portfolio"
          >
            <FaHome className="leftcontainerIcons"/> Portfolio
          </a>
        </div>
      </div>

      <div className="middleContainer">
        <div className="app">{renderScreen()}</div>
        <div className="bottom">
          <div className="mainpage" onClick={clickedHomePage}>
            <FaHome className="bottomicon mainpageicon" />
            Ana Sayfa
          </div>

          <div className="analayzepage" onClick={clickedAnalayzePage}>
            <IoAnalytics className="bottomicon analayzeicon" />
            Analiz
          </div>

          <div className="profilepage" onClick={clickedProfilePage}>
            <CgProfile className="bottomicon profileicon" />
            Profil
          </div>
        </div>
      </div>

      <div className="rightContainer">
        <h2>Sağ Bölüm</h2>
        <p>Ekstra bilgiler burada bulunabilir.</p>
      </div>
    </div>
  );
}

export default App;
