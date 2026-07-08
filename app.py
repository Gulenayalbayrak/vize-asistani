import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF Fonksiyonu
def pdf_olustur(ulke, secilenler, ihtimal, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{ulke} Vize Analiz Raporu", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Onay Ihtimali: %{ihtimal}", ln=True)
    pdf.cell(200, 10, txt=f"Tahmini Toplam Maliyet: {data['harc'] + data['servis']} Euro", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Sunulan Belgeler:", ln=True)
    pdf.set_font("Arial", size=12)
    for doc in secilenler:
        pdf.cell(200, 10, txt=f"- {doc}", ln=True)
    file_name = "vize_raporu.pdf"
    pdf.output(file_name)
    return file_name

# Sayfa Yapılandırması
st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Veri Tabanı
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 25€"},
    "İspanya": {"onay": 82, "harc": 90, "servis": 30, "ekstra": "Ekspres Fark: 40€, Sigorta: 20€"},
    "İtalya": {"onay": 78, "harc": 80, "servis": 30, "ekstra": "Randevu Ücreti: 20€, Sigorta: 25€"}
}
tum_evraklar = ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu", "Otel Rezervasyonu", "Banka Hesap Dökümü", "Maaş Bordrosu"]
ZORUNLU = ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu"]

# Otomatik Geçiş İçin Session State
if 'nav' not in st.session_state:
    st.session_state.nav = "Hoş Geldiniz"

# Yan Menü (Sidebar)
menu_options = ["Hoş Geldiniz", "Belgelerim", "Analiz", "Maliyet & Uyarı"]
secim = st.sidebar.radio("Navigasyon:", menu_options, index=menu_options.index(st.session_state.nav), key="nav")

# Sayfalar
if secim == "Hoş Geldiniz":
    st.title("✈️ Vize Uzmanı Portalı")
    st.write("Belgelerinizi hazırlayın, onay ihtimalinizi ölçün.")

elif secim == "Belgelerim":
    st.title("📄 Belgelerim")
    ulke = st.selectbox("Ülke Seçiniz:", list(ulke_verileri.keys()))
    st.session_state.ulke = ulke
    
    secilenler = []
    cols = st.columns(3)
    for i, evrak in enumerate(tum_evraklar):
        if cols[i % 3].checkbox(evrak, key=evrak): secilenler.append(evrak)
    
    if st.button("Analize Git ->"):
        if [b for b in ZORUNLU if b not in secilenler]:
            st.error("❌ Eksik zorunlu belgeler var!")
        else:
            st.session_state.secilenler = secilenler
            st.session_state.nav = "Analiz"
            st.rerun()

elif secim == "Analiz":
    st.title("📊 Analiz Sonucu")
    if 'secilenler' in st.session_state:
        ulke = st.session_state.ulke
        ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.secilenler) * 2), 98)
        st.metric("Tahmini Onay İhtimali", f"%{round(ihtimal, 1)}")
        st.progress(ihtimal/100)
        
        if st.button("Raporu İndir"):
            pdf_dosyasi = pdf_olustur(ulke, st.session_state.secilenler, round(ihtimal, 1), ulke_verileri[ulke])
            with open(pdf_dosyasi, "rb") as f:
                st.download_button("PDF İndir", f, file_name=pdf_dosyasi, mime="application/pdf")
    else:
        st.warning("Önce 'Belgelerim' sekmesinden seçim yapın!")

elif secim == "Maliyet & Uyarı":
    st.title("⚠️ Maliyet ve Uyarı")
    if 'ulke' in st.session_state:
        data = ulke_verileri[st.session_state.ulke]
        st.write(f"**Ülke:** {st.session_state.ulke}")
        st.write(f"**Vize Harcı:** {data['harc']}€ | **Ekstralar:** {data['ekstra']}")
    else:
        st.warning("Ülke seçimi yapılmadı.")