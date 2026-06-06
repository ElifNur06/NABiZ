# 🫀 NABIZ (HardwareAwareMem Core)

**Otonom Donanım-Farkındalıklı Dağıtık Sistemler Çekirdeği** Yazılım mimarilerini, üzerinde çalıştıkları donanımın fiziksel gerçekliğiyle (ısı, güç, işlemci yükü) senkronize eden, proaktif ve otonom bir sistem optimizasyon motoru.

*Not: Nabız'ın çekirdek algoritmaları, JIT motoru ve öngörücü yapay zeka altyapısı fikri mülkiyet hakları kapsamında kapalı kaynak (private) olarak korunmaktadır. Bu doküman, sistemin teknik kapasitesini ve mimari vizyonunu özetlemektedir.*

---

## 📖 Vizyon ve Felsefe

Günümüz standart yazılım mimarileri, işletim sistemi ısındığında veya cihaz güç kaybettiğinde "hiçbir şey olmamış gibi" aynı agresif hızda bellek tüketmeye ve döngüleri çalıştırmaya devam eder. Bu körlük; sunucu çöküşlerine, mobil cihazlarda bataryanın aniden tükenmesine ve donanımın termal hasar almasına yol açar.

**Nabız**, yazılım ile donanım arasına zeka koyar. Sistem reaktif (panik odaklı) değil, **proaktif (öngörücü)** bir yaklaşımla çalışır. Cihazın ısınacağını veya bataryasının tükeneceğini saniyeler önceden hesaplayarak, uygulamanın kendi bellek ve yürütme mimarisini çalışma anında (runtime) otonom olarak değiştirir.

---

## 🧠 Çekirdek Sistem Mimarisi

Sistemin kalbi, işletim sistemini yormadan asenkron olarak çalışan iki ana mimariden oluşur:

### 1. Proaktif "Öngörücü" Yapay Zeka Karar Motoru
Nabız, sadece o anki sıcaklık veya işlemci yüküne bakmaz. 
* **Zaman Serisi Analizi:** Sensör verilerini dairesel tamponlarda (circular buffer) biriktirir.
* **Trend Kestirimi:** En küçük kareler yöntemi (Least Squares) ile sıcaklık değişim ivmesini hesaplar. İşlemci anlık 55°C olsa bile, eğim çok yüksekse motor bunu algılar ve *"15 saniye içinde donanım 90°C'ye ulaşacak"* diyerek sistemi anında güvenli moda geçirir.

### 2. Dinamik Bellek Stratejileri (Memory Modes)
Uygulamanın bellek yönetimi, donanımın anlık sağlığına göre üç farklı boyutta şekillenir:
* **🚀 Performance Modu:** Sistem serin ve şarjdayken çalışır. Çöp toplayıcı (Garbage Collector) baskılanır, RAM'den maksimum tahsisat yapılır. Döngüler en yüksek hızda çalışır.
* **⚖️ Balanced Modu:** Standart günlük kullanım. Dengeli nesne yaratımı ve standart RAM temizlik kuralları işletilir.
* **🛡️ Eco/Thermal Modu:** Donanım ısındığında veya pil kritik seviyeye düştüğünde devreye girer. Otomatik GC tamamen kapatılır. İşletim sisteminden yeni RAM istenmez; önceden ayrılmış **Nesne Havuzu (Object Pool)** kullanılarak sadece var olan bellek blokları geri dönüştürülür. İşlemci üzerindeki tahsisat (allocation) yükü sıfırlanır.

---

## ⚙️ İleri Seviye Koruma ve Entegrasyon Modülleri

Nabız, sadece RAM yönetmekle kalmaz, uygulamanın dış dünyayla ve çalışma zamanıyla (runtime) olan tüm ilişkisini kontrol eder.

### JIT Motoru ve Yorumlayıcı Entegrasyon Köprüsü
Kodun yürütülme katmanına doğrudan müdahale eden kalkan. Sistem `Eco/Thermal` moda geçtiğinde, işlemciyi yoran ağır hesaplama döngülerini (heavy computation loops) anında durdurur. İşlemciyi yakmak yerine, daha önceden hesaplanmış, önbelleğe alınmış (cached) veya güvenli varsayılan (fallback) sonuçları döndürerek donanıma saniyesinde nefes aldırır.

### Çevrimdışı-Öncelikli (Offline-First) Edge Optimizasyonu
Ağ çağrılarının ve dış API işlemlerinin mobil/IoT cihazlarda yarattığı ısı ve pil tüketimini engeller. Cihaz strese girdiğinde, dışa dönük tüm veri aktarımlarını durdurup yerel kuyruğa (local queue) alır. Sistem soğuduğunda ve güvende olduğunda, arka planda çalışan otonom bir işçi biriken verileri topluca (batch) buluta senkronize eder. Sıfır veri kaybı, maksimum donanım ömrü.

### Merkezi Telemetri ve BaaS Uyumu (Otonom Yük Dağıtımı)
FastAPI tabanlı backend sunucularına entegre edilen donanım-farkındalıklı *Middleware*. Bir sunucu düğümü (node) kapasitesini aştığında veya ısınma trendine girdiğinde, gelen HTTP isteklerini anında `503 Service Unavailable` ile reddeder. Çökmeyi beklemeden kendini izole eder ve merkezi Yük Dağıtıcının (Load Balancer) trafiği anında filodaki diğer serin sunuculara yönlendirmesini sağlar.

---
## Görseller
<img width="1427" height="805" alt="image" src="https://github.com/user-attachments/assets/26ce1e8b-b63b-4c2f-9c58-28436b4fc226" />
<img width="1428" height="805" alt="image" src="https://github.com/user-attachments/assets/3fa3bb88-6ec7-4355-a21f-ad00394cdacf" />
<img width="1428" height="803" alt="image" src="https://github.com/user-attachments/assets/e92a9f35-b3d9-4a0c-ad11-9fe774df1bd6" />
<img width="1427" height="802" alt="image" src="https://github.com/user-attachments/assets/3ab2d2d2-0862-4972-b742-0c3ef0c1eb06" />
<img width="1429" height="803" alt="image" src="https://github.com/user-attachments/assets/2c4bc969-c93f-4790-b597-fef2fc6f2ded" />
<img width="1427" height="803" alt="image" src="https://github.com/user-attachments/assets/7bda2e18-9ee8-42fc-854d-6d3afad1ab7f" />
<img width="1428" height="801" alt="image" src="https://github.com/user-attachments/assets/c188236c-7938-4ae0-a4b3-3e2db48ba33b" />
<img width="1427" height="805" alt="image" src="https://github.com/user-attachments/assets/4b980a3e-2e72-497e-89fb-bebb2508d767" />
<img width="1428" height="804" alt="image" src="https://github.com/user-attachments/assets/bf5b4493-ce6a-4e0e-a843-d522e67f9831" />
<img width="1428" height="805" alt="image" src="https://github.com/user-attachments/assets/cda58fde-c1a3-42bd-afca-e70d43a15757" />


## 💥 Kıyamet Senaryosu (Doomsday) Direnci

Sistem, "Bellek Bombası" (Memory Bomb) ve "Termal Kaçak" (Thermal Runaway) gibi ekstrem saldırı ve kriz anlarında hayatta kalmak üzere tasarlanmıştır:
* İşlemci %100 yüke sokulup sıcaklık eksponansiyel arttığında, proaktif motor saniyeler öncesinden bağlantıları kilitler.
* Eco moddayken dışarıdan gelen binlerce nesnelik RAM talebi, işletim sistemini kilitlemeden absorbe edilir ve donanımı korumak adına acımasızca reddedilir (*Graceful Degradation*).

---

## 🌌 Ekosistem: Yankı ve Kardelen

Nabız, kendi başına bir kütüphane olmasının ötesinde, devasa bir vizyonun **otonom hayatta kalma çekirdeğidir**.

* **Yankı (Nexus BaaS) Filo Yönetimi:** Nabız, Yankı'nın merkezi telemetri omurgasıdır. Yankı sunucu filolarındaki ısınan makineleri proaktif olarak izole edip otonom yük dağıtımı sağlayarak %100 kesintisiz (High Availability) hizmet sunmasının arkasındaki güçtür.
* **Kardelen Yorumlayıcısı:** Nabız'ın JIT köprüsü, Kardelen programlama dilinin yorumlayıcısı içinde **Self-Optimizing LLM-Driven** bir kalkan olarak yer alır. Kardelen'i; donanımın acısını hisseden, aşırı ısınmada ağır döngüleri atlayıp optimize edilmiş çıktıları sunabilen "yaşayan" bir dile dönüştürür.

---
**Geliştirici:** Elif Nur Ayhan  
**Durum:** Üretime Hazır (Production-Ready)  
**Telif Hakkı:** Tüm çekirdek algoritmalar ve mimari tasarımlar gizlidir ve fikri mülkiyet hakları saklıdır.
