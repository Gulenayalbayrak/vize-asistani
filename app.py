import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF Fonksiyonu
def pdf_olustur(ulke, secilenler, ihtimal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{ulke} Vize Analiz Raporu", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Onay Ihtimali: %{ihtimal}", ln=True)
    for doc in secilenler:
        pdf.cell(200, 10, txt=f"- {doc}", ln=True)
    file_name = "vize_raporu.pdf"
    pdf.output(file_name)
    return file_name

st.set_page_config(page_title="Vize Uzmani", layout="wide")

# Tüm veriler
ulke_verileri = {
    "Almanya": 85, "Ispanya": 82, "Italya": 78, "Fransa": 75, 
    "Hollanda": 88, "Belcika": 70, "Yunanistan": 92
}
tum_evraklar = [
    "Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu", "Otel Rezervasyonu", 
    "Banka Hesap Dokumu", "Maas Bordrosu", "Tapu", "Arac Ruhsati",
    "Isyeri Izin", "Vergi Levhasi", "Davetiye", "Fotograf"
]
ZORUNLU = ["Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu"]

# Otomatik yönlendirme için State yönetimi
if 'nav' not in st.session_state: st.session_state.nav = "Belgelerim"

# Menü
nav = st.radio("Navigasyon:", ["Belgelerim", "Analiz"], index=["Belgelerim", "Analiz"].index(st.session_state.nav), horizontal=True)

if nav == "Belgelerim":
    st.title("📄 Belgelerim")
    ulke = st.selectbox("Ulke:", list(ulke_verileri.keys()))
    secilenler = []
    cols = st.columns(3)
    for i, evrak in enumerate(tum_evraklar):
        if cols[i % 3].checkbox(evrak, key=evrak): secilenler.append(evrak)
    
    if st.button("Analize Git ->"):
        eksikler = [b for b in ZORUNLU if b not in secilenler]
        if eksikler:
            st.error(f"Eksik zorunlu belgeler: {', '.join(eksikler)}")
        else:
            st.session_state.secilenler = secilenler
            st.session_state.secilen_ulke = ulke
            st.session_state.nav = "Analiz"
            st.rerun()

elif nav == "Analiz":
    if 'secilenler' in st.session_state:
        st.title("📊 Analiz Sonucu")
        ulke = st.session_state.secilen_ulke
        ihtimal = min(ulke_verileri[ulke] + (len(st.session_state.secilenler) * 2), 98)
        st.metric("Onay Ihtimali", f"%{ihtimal}")
        st.progress(ihtimal/100)
        
        pdf_dosyasi = pdf_olustur(ulke, st.session_state.secilenler, ihtimal)
        with open(pdf_dosyasi, "rb") as f:
            st.download_button("Raporu Indir", f, file_name=pdf_dosyasi, mime="application/pdf")
    else:
        st.warning("Lutfen once belgeleri secin!")