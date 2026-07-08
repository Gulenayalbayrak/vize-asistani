from foundry_local_sdk import FoundryLocalManager, Configuration
import sqlite3
import json

print("--- 1. ADIM: Model Yükleniyor ---")
manager = FoundryLocalManager(config=Configuration(app_name="MyRagAssistant"))
models = manager.catalog.list_models()
target_model = models[18] 
target_model.load()
chat = target_model.get_chat_client()
print("Model yüklendi.")

print("--- 2. ADIM: Veritabanı Kuruluyor ---")
conn = sqlite3.connect('vize_asistani.db')
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS notlar')
cursor.execute('CREATE TABLE IF NOT EXISTS notlar (id INTEGER PRIMARY KEY, metin TEXT, vektor TEXT)')

vize_notlari = [
    "Almanya vizesi: Seyahat sağlık sigortası poliçe süresi, kalış süresini mutlaka kapsamalıdır.",
    "İspanya vizesi: Otel rezervasyonu tüm seyahat günlerini kapsamalı ve onaylı olmalıdır.",
    "Genel kural: Öğrenci vizesinde güncel öğrenci belgesi, sponsor banka dökümü ve okul davet mektubu şarttır."
]

for i, metin in enumerate(vize_notlari):
    cursor.execute('INSERT INTO notlar (metin, vektor) VALUES (?, ?)', (metin, json.dumps([0.0])))
conn.commit()
print("Notlar veritabanına eklendi.")

def vize_asistani(soru):
    print(f"Sorgulanıyor: {soru}")
    cursor.execute('SELECT metin FROM notlar')
    tum_notlar = cursor.fetchall()
    
    soru_lower = soru.lower()
    secilen_bilgi = None
    
    if "almanya" in soru_lower:
        secilen_bilgi = tum_notlar[0][0]
    elif "ispanya" in soru_lower:
        secilen_bilgi = tum_notlar[1][0]
    elif "genel" in soru_lower or "öğrenci vizesi" in soru_lower:
        secilen_bilgi = tum_notlar[2][0]
    
    if secilen_bilgi is None:
        return "Üzgünüm, bu konuda bilgim yok."
        
    prompt = f"Sadece şu bilgiyi kullan: '{secilen_bilgi}'. Soru: '{soru}'"
    response = chat.complete_chat([{"role": "user", "content": prompt}])
    return response.choices[0].message.content

print("--- 3. ADIM: Test Başlıyor ---")
print("Cevap 1:", vize_asistani("Almanya vizesi için ne gerekir?"))
print("Cevap 2:", vize_asistani("Fransa vizesi için ne gerekir?"))

conn.close()