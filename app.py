import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF oluşturma fonksiyonu güncellendi (Yeni alanlar eklendi)
def pdf_olustur(ulke, data, secilen_evraklar, yeni_ihtimal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    baslik = f"{ulke} Vize Analiz ve Bilgi Raporu".encode('latin-1', 'replace').decode('latin-1')
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
        
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Yasal Uyari ve Ekstra Maliyetler:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt="Vize ucreti disinda; yurtdisi cikis harci, konsolosluk servis bedelleri, kargo masraflari ve olasi eksik belge cezalarina karsi hazirlikli olunmalidir.")
    
    file_name = "vize_kapsamli_rapor.pdf"
    pdf.output(file_name)
    return file_name

# Sayfa Yapılandırması
st.set_page_config(page_title="Vize Uzmani Pro", layout="wide")

# Veri Yapısı (Ekstra maliyetler eklendi)
ulke_bilgileri = {
    "Almanya": {"onay": 85, "ekstra": "Yurtdisi Cikis Harci: 500 TL, Kargo: 15 Euro, Danismanlik Hizmeti: 50 Euro"},
    "Ispanya": {"onay": 82, "ekstra": "Yurtdisi Cikis Harci: 500 TL, Ekspres Basvuru Farkı: 40 Euro"},
    "Italya": {"onay": 78, "ekstra": "Yurtdisi Cikis Harci: 500 TL, Konsolosluk Randevu Ucreti: 20 Euro"}
}

tum_evraklar = [
    "Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu", "Otel Rezervasyonu", 
    "Banka Hesap Dokumu", "Maas Bordrosu", "Tapu Fotokopisi", "Arac Ruhsati",
    "Isyeri Izin Belgesi", "Vergi Levhasi", "Davetiye", "Fotograf"
]

st.title("🌍 Vize Uzmani: Akilli Analiz ve Rehber")
ulke = st.selectbox("Ulke Seciniz:", list(ulke_bilgileri.keys()))

# 3 Sekmeli Yapı
tab1, tab2, tab3 = st.tabs(["📄 Belgelerim", "📊 Analiz", "⚠️ Yasal Bilgiler"])

with tab1:
    st.subheader("Elinde Olan Belgeleri Sec:")
    secilenler = []
    cols = st.columns(3)
    for i, evrak in enumerate(tum_evraklar):
        if cols[i % 3].checkbox(evrak):
            secilenler.append(evrak)

with tab2:
    base_onay = ulke_bilgileri[ulke]["onay"]
    yeni_onay = min(base_onay + (len(secilenler) * 0.8), 98)
    st.metric("Tahmini Vize Onay Ihtimali", f"%{round(yeni_onay, 1)}")
    st.progress(yeni_onay/100)
    
    if st.button("Analiz Raporunu PDF Olarak Indir"):
        pdf_dosyasi = pdf_olustur(ulke, ulke_bilgileri[ulke], secilenler, round(yeni_onay, 1))
        with open(pdf_dosyasi, "rb") as f:
            st.download_button("Indir", f, file_name=pdf_dosyasi, mime="application/pdf")

with tab3:
    st.subheader(f"⚠️ {ulke} Icin Kritik Uyarlar")
    st.warning("Vize basvurularinda verilen yanlis beyanlar, 'vize yasagi' cezasi almaniza neden olabilir.")
    st.info(f"Ekstra Tahmini Maliyetler: {ulke_bilgileri[ulke]['ekstra']}")
    st.markdown("""
    **Bilinmesi Gerekenler:**
    - **Yurtdışı Çıkış Harcı:** Tüm ülkeler için geçerlidir.
    - **Cezai Durum:** Eksik belge sunmak vize reddine ve harç ücretinin yanmasına sebep olur.
    - **Önemli Not:** Seyahat sigortası poliçesinin seyahat tarihlerini kapsaması zorunludur.
    """)