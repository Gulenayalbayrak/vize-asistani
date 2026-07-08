import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF oluşturma fonksiyonu (Değişmedi)
def pdf_olustur(ulke, data, secilen_evraklar, yeni_ihtimal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    baslik = f"{ulke} Vize Basvuru Raporu".encode('latin-1', 'replace').decode('latin-1')
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

# Zorunlu belgeler listesi
ZORUNLU_BELGELER = ["Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu"]

ulke_bilgileri = {
    "Almanya": {"onay": 85, "ekstra": "Kargo: 15 Euro"},
    "Ispanya": {"onay": 82, "ekstra": "Ekspres Fark: 40 Euro"},
    "Italya": {"onay": 78, "ekstra": "Randevu Ucreti: 20 Euro"}
}

tum_evraklar = [
    "Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu", "Otel Rezervasyonu", 
    "Banka Hesap Dokumu", "Maas Bordrosu", "Davetiye", "Fotograf"
]

st.title("🌍 Vize Uzmani: Akilli Kontrol Sistemi")
ulke = st.selectbox("Ulke Seciniz:", list(ulke_bilgileri.keys()))

# Session State ile sayfa kontrolü
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "Belgelerim"

tab1, tab2, tab3 = st.tabs(["📄 Belgelerim", "📊 Analiz", "⚠️ Yasal Bilgiler"])

with tab1:
    st.subheader("Elinde Olan Belgeleri Sec:")
    secilenler = []
    cols = st.columns(3)
    for i, evrak in enumerate(tum_evraklar):
        if cols[i % 3].checkbox(evrak, key=evrak):
            secilenler.append(evrak)
    
    # Devam Et Butonu
    if st.button("Analize Git ->"):
        # Zorunlu kontrolü
        eksikler = [b for b in ZORUNLU_BELGELER if b not in secilenler]
        if eksikler:
            st.error(f"Eksik belgeler var: {', '.join(eksikler)}. Lutfen kontrol ediniz!")
        else:
            st.success("Tüm zorunlu belgeler tamam! Analiz sekmesine geçebilirsiniz.")
            st.session_state.secilenler = secilenler # Analiz için veriyi sakla

with tab2:
    st.subheader("Vize Analiz Sonucu")
    if 'secilenler' in st.session_state:
        base_onay = ulke_bilgileri[ulke]["onay"]
        yeni_onay = min(base_onay + (len(st.session_state.secilenler) * 2), 98)
        st.metric("Tahmini Vize Onay Ihtimali", f"%{round(yeni_onay, 1)}")
        st.progress(yeni_onay/100)
        
        if st.button("Raporu Indir"):
            pdf_dosyasi = pdf_olustur(ulke, ulke_bilgileri[ulke], st.session_state.secilenler, round(yeni_onay, 1))
            with open(pdf_dosyasi, "rb") as f:
                st.download_button("Indir", f, file_name=pdf_dosyasi, mime="application/pdf")
    else:
        st.warning("Lutfen once belgelerinizi secip analize baslayin.")

with tab3:
    st.info(f"Ekstra Tahmini Maliyetler: {ulke_bilgileri[ulke]['ekstra']}")