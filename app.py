import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF oluşturma fonksiyonu
def pdf_olustur(ulke, data, secilen_evraklar, yeni_ihtimal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    baslik = f"{ulke} Vize Analiz Raporu".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(200, 10, txt=baslik, ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Guncellenmis Onay Ihtimali: %{yeni_ihtimal}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Sunulan Belgeler:", ln=True)
    pdf.set_font("Arial", size=12)
    for doc in secilen_evraklar:
        pdf.cell(200, 10, txt=f"- {doc}", ln=True)
    
    file_name = "vize_analiz_raporu.pdf"
    pdf.output(file_name)
    return file_name

# Sayfa Yapılandırması
st.set_page_config(page_title="Vize Uzmani Pro", layout="wide")

# Veritabanı ve Evrak Havuzu
tum_evraklar = [
    "Pasaport", "Sigorta Poliçesi", "Ucak Rezervasyonu", "Otel Rezervasyonu", 
    "Banka Hesap Dokumu", "Maas Bordrosu", "Tapu Fotokopisi", "Arac Ruhsati",
    "Isyeri Izin Belgesi", "Vergi Levhasi", "Davetiye", "Fotograf",
    "Adli Sicil Kaydi", "Tam Tekmil Vukuatli Nufus Kayit Ornegi", "Ikametgah",
    "Askerlik Durum Belgesi", "Diploma", "Kredi Karti Ekstresi"
]

ulke_verileri = {
    "Almanya": {"onay": 85}, "Ispanya": {"onay": 82}, "Italya": {"onay": 78}
}

st.title("🌍 Vize Uzmani: Akilli Analiz")
ulke = st.selectbox("Ulke Seciniz:", list(ulke_verileri.keys()))

# 15-20 Seçenekli Checkbox Listesi
st.subheader("Elinde Olan Belgeleri Sec:")
secilenler = []
cols = st.columns(3) # Ekranı 3 sütuna bölerek şık görünüm sağladık
for i, evrak in enumerate(tum_evraklar):
    if cols[i % 3].checkbox(evrak):
        secilenler.append(evrak)

# Onay İhtimali Hesaplama Mantığı (Basit bir puanlama)
base_onay = ulke_verileri[ulke]["onay"]
yeni_onay = min(base_onay + (len(secilenler) * 0.5), 98) # Her belge %0.5 artırır

st.write("---")
st.metric("Tahmini Vize Onay Ihtimali", f"%{round(yeni_onay, 1)}")
st.progress(yeni_onay/100)

# PDF İndirme
if st.button("Analiz Raporunu PDF Olarak Indir"):
    pdf_dosyasi = pdf_olustur(ulke, ulke_verileri[ulke], secilenler, round(yeni_onay, 1))
    with open(pdf_dosyasi, "rb") as f:
        st.download_button("Indir", f, file_name=pdf_dosyasi, mime="application/pdf")