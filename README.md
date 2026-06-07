# 🛡️ Siber Güvenlik : Merkle-Hellman & E2EE Ağ Tüneli

Bu proje, asimetrik şifreleme algoritmalarının hem **sunucu tabanlı (Cloud)** dosya şifrelemesinde hem de **istemci tabanlı (Client-Side)** Uçtan Uca Şifreli (E2EE) anlık ağ iletişiminde nasıl kullanılacağını uygulamalı olarak gösteren kapsamlı bir siber güvenlik süitidir.

Modern bir UI/UX (Glassmorphism) yaklaşımıyla tasarlanan arayüz, arka planda saf matematik ve soket programlama mimarilerini barındırır.

---

## 🚀 Proje Mimarisi ve Özellikler

Proje "Hepsi Bir Arada" mantığıyla sekmeli (tab) bir yapı üzerine kurulmuştur ve iki ana modülden oluşur:

### 📁 Modül 1: Dosya ve Metin Şifreleme (Server-Side)
Bulut tabanlı asimetrik şifreleme ve kriptanaliz laboratuvarı.

* **Merkle-Hellman Sırt Çantası Algoritması:** Hazır şifreleme kütüphaneleri (AES/RSA modülleri vb.) yerine, tamamen `Genişletilmiş Öklid` ve `Modüler Ters Alma` algoritmaları kullanılarak sıfırdan yazılmış asimetrik motor.
* **Kriptanaliz ve Güvenlik Skoru:** Üretilen rastgele anahtarların "Sırt Çantası Yoğunluğunu (Knapsack Density)" matematiksel olarak hesaplar. Eğer yoğunluk `0.94`'ten küçükse, sistemin *LLL (Lenstra–Lenstra–Lovász)* saldırılarına açık olduğuna dair dinamik uyarı verir.
* **Bayt Seviyesinde Dosya Koruması:** `.jpg`, `.pdf`, `.txt` vb. herhangi bir dosyayı `Base64` dönüşümü ile bayt seviyesinde şifreler, `.enc` formatında güvenli olarak dışa aktarır ve orijinal formuna kayıpsız döndürür.
* **Anahtar Yönetim Merkezi:** Üretilen Açık (Public) ve Kapalı (Private) anahtarların JSON formatında cihaza yedeklenmesini ve daha sonra sisteme yüklenmesini sağlar.

### 💬 Modül 2: Uçtan Uca Şifreli (E2EE) Ağ Tüneli (Client-Side)
WhatsApp ve Signal gibi uygulamaların temelini oluşturan sıfır bilgi ispatlı ağ haberleşmesi.

* **İstemci Tabanlı Şifreleme (Client-Side Cryptography):** Tüm Merkle-Hellman şifreleme ve çözme algoritmaları JavaScript ile doğrudan tarayıcıda çalışır.
* **Sıfır Bilgi İspatı (Zero-Knowledge):** Flask Python sunucusu yalnızca kör bir yönlendirici (Router) görevi görür. Mesajların içeriğini, şifreleri veya anahtarları asla bilemez.
* **Güvenli Anahtar Takası (Handshake):** Ağa katılan cihazlar arka planda otomatik olarak açık anahtarlarını takas eder. Sonsuz döngü ve yayın fırtınasını (Broadcast Storm) engelleyen eşler arası hafıza (Peers Memory) yönetimine sahiptir.
* **Çapraz Çözümleme (Cross-Decryption) Koruması:** Ağda birden fazla cihaz (sekme) olduğunda, paketler hedef etiketleriyle yollanır. Böylece cihazlar sadece kendilerine gelen paketleri çözmeye çalışarak "Bozuk Paket" hatalarını engeller.
* **Entegre Ağ İzleyici (Packet Sniffer):** Arayüzde bulunan Wireshark benzeri canlı ağ paneli üzerinden, ağ (Network) katmanından sadece `[241, 632, 910...]` gibi şifreli rakam bloklarının geçtiği eşzamanlı olarak izlenebilir. (16-bit UTF-16 destekli).

---

## 🛠️ Kullanılan Teknolojiler

* **Backend:** Python, Flask, Flask-SocketIO (WebSocket)
* **Frontend:** HTML5, Vanilla JavaScript, CSS3 (Glassmorphism & Toast UI)
* **Kriptografi:** Merkle-Hellman Knapsack Cryptosystem, Extended Euclidean Algorithm
* **Ağ (Networking):** TCP/IP, WebSocket (Full-Duplex gerçek zamanlı iletişim)

---

## ⚙️ Kurulum ve Çalıştırma

Projeyi yerel bilgisayarınızda çalıştırmak için aşağıdaki adımları izleyin:

**1. Depoyu Klonlayın veya İndirin:**
```bash
git clone <sizin_repo_linkiniz>
cd <proje_klasor_adi>

2. Gerekli Kütüphaneleri Kurun:
Projenin ağ yönlendirme işlemlerini yapabilmesi için Flask ve Socket.IO modüllerine ihtiyacı vardır.

Bash
pip install flask flask-socketio
3. Sunucuyu Başlatın:

Bash
python app.py
(Terminalde "SİBER GÜVENLİK SÜİTİ BAŞLATILDI" mesajını görmelisiniz.)

4. Arayüze Erişin:

Tarayıcınızı açın ve http://127.0.0.1:5000 adresine gidin.

E2EE Ağını (Modül 2) test etmek için: Tarayıcınızda iki farklı sekme veya pencere açıp ekranı ikiye bölün. Sekmelerin otomatik olarak "El Sıkışma (Handshake)" yaptığını göreceksiniz. Birinden yazdığınız mesaj, ağ üzerinden şifreli rakamlar olarak geçer ve diğerinde çözülür.
