import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF Fonksiyonu (Hem Analiz hem Maliyet içerecek şekilde)
def pdf_olustur(ulke, secilenler, ihtimal, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{ulke} Vize Analiz ve Maliyet Raporu", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Onay Ihtimali: %{ihtimal}", ln=True)
    pdf.cell(200, 10, txt=f"Tahmini Maliyet: {data['harc'] + data['servis']} Euro", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Sunulan Belgeler:", ln=True)
    pdf.set_font("Arial", size=12)
    for doc in secilenler:
        pdf.cell(200, 10, txt=f"- {doc}", ln=True)
    file_name = "vize_raporu.pdf"
    pdf.output(file_name)
    return file_name

st.set_page_config(page_title="Vize Uzmani", layout="wide")

# Veriler (Ücretler ve Ekstralar geri eklendi)
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 25€"},
    "Ispanya": {"onay": 82, "harc": 90, "servis": 30, "ekstra": "Ekspres Fark: 40€, Sigorta: 20€"},
    "Italya": {"onay": 78, "harc": 80, "servis": 30, "ekstra": "Randevu Ücreti: 20€, Sigorta: 25€"},
    "Fransa": {"onay": 75, "harc": 80, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 20€"},
    "Hollanda": {"onay": 88, "harc": 90, "servis": 30, "ekstra": "Sigorta: 25€"},
    "Belcika": {"onay": 70, "harc": 90, "servis": 30, "ekstra": "Sigorta: 20€"},
    "Yunanistan": {"onay": 92, "harc": 80, "servis": 30, "ekstra": "Sigorta: 20€"}
}
tum_evraklar = ["Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu", "Otel Rezervasyonu", "Banka Hesap Dokumu", "Maas Bordrosu", "Davetiye", "Fotograf"]
ZORUNLU = ["Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu"]

# Navigasyon
if 'nav' not in st.session_state: st.session_state.nav = "Belgelerim"
nav = st.radio("Sayfalar:", ["Belgelerim", "Analiz", "Maliyet & Uyari"], index=["Belgelerim", "Analiz", "Maliyet & Uyari"].index(st.session_state.nav), horizontal=True)
st.session_state.nav = nav

# --- SAYFA 1 ---
if nav == "Belgelerim":
    st.title("📄 Belgelerim")
    ulke = st.selectbox("Ulke:", list(ulke_verileri.keys()))
    secilenler = []
    cols = st.columns(3)
    for i, evrak in enumerate(tum_evraklar):
        if cols[i % 3].checkbox(evrak, key=evrak): secilenler.append(evrak)
    
    if st.button("Analize Git ->"):
        if [b for b in ZORUNLU if b not in secilenler]:
            st.error("Eksik zorunlu belgeler var!")
        else:
            st.session_state.secilenler = secilenler
            st.session_state.secilen_ulke = ulke
            st.session_state.nav = "Analiz"
            st.rerun()

# --- SAYFA 2 ---
elif nav == "Analiz":
    st.title("📊 Analiz Sonucu")
    if 'secilenler' in st.session_state:
        ulke = st.session_state.secilen_ulke
        ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.secilenler) * 2), 98)
        st.metric("Onay Ihtimali", f"%{ihtimal}")
        st.progress(ihtimal/100)
        
        if st.button("Raporu Indir"):
            pdf_dosyasi = pdf_olustur(ulke, st.session_state.secilenler, ihtimal, ulke_verileri[ulke])
            with open(pdf_dosyasi, "rb") as f:
                st.download_button("Indir", f, file_name=pdf_dosyasi, mime="application/pdf")
    else:
        st.warning("Once belgeleri secin!")

# --- SAYFA 3 ---
elif nav == "Maliyet & Uyari":
    st.title("⚠️ Maliyet ve Yasal Uyari")
    ulke = st.session_state.get('secilen_ulke', 'Almanya')
    data = ulke_verileri[ulke]
    st.info(f"Seçilen Ülke: {ulke}")
    st.write(f"**Vize Harcı:** {data['harc']}€ | **Servis:** {data['servis']}€")
    st.write(f"**Ekstralar:** {data['ekstra']}")
    st.warning("Yalan beyan vize yasağına yol açar. Belgelerinizin doğruluğundan emin olun.")