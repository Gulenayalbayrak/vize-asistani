import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF fonksiyonu
def pdf_olustur(ulke, secilenler, ihtimal, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{ulke} Vize Analiz Raporu", ln=True, align='C')
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

# Veriler
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 25€"},
    "Ispanya": {"onay": 82, "harc": 90, "servis": 30, "ekstra": "Ekspres Fark: 40€, Sigorta: 20€"},
    "Italya": {"onay": 78, "harc": 80, "servis": 30, "ekstra": "Randevu Ücreti: 20€, Sigorta: 25€"}
}
tum_evraklar = ["Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu", "Otel Rezervasyonu", "Banka Hesap Dokumu", "Maas Bordrosu"]
ZORUNLU = ["Pasaport", "Sigorta Policesi", "Ucak Rezervasyonu"]

# --- SIDEBAR (YAN MENÜ) ---
st.sidebar.title("🌍 Vize Uzmani Menü")
secim = st.sidebar.radio("Git:", ["Hoş Geldiniz", "Belgelerim", "Analiz", "Maliyet & Uyarı"])

# --- HOŞ GELDİNİZ EKRANI ---
if secim == "Hoş Geldiniz":
    st.title("✈️ Vize Uzmanı Portalı'na Hoş Geldiniz!")
    st.write("Bu uygulama ile vize süreçlerinizi kolayca planlayabilir, belge listenizi kontrol edebilir ve onay ihtimalinizi analiz edebilirsiniz.")
    st.info("Başlamak için yan menüden 'Belgelerim' sekmesine geçebilirsiniz.")

# --- DİĞER SAYFALAR ---
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
            st.error("Eksik zorunlu belgeler var!")
        else:
            st.session_state.secilenler = secilenler
            st.success("Belgeler onaylandı! Yan menüden 'Analiz' sekmesine geçebilirsiniz.")

elif secim == "Analiz":
    st.title("📊 Analiz Sonucu")
    if 'secilenler' in st.session_state:
        ulke = st.session_state.ulke
        ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.secilenler) * 2), 98)
        st.metric("Onay İhtimali", f"%{ihtimal}")
        st.progress(ihtimal/100)
        
        if st.button("Raporu İndir"):
            pdf_dosyasi = pdf_olustur(ulke, st.session_state.secilenler, ihtimal, ulke_verileri[ulke])
            with open(pdf_dosyasi, "rb") as f:
                st.download_button("İndir", f, file_name=pdf_dosyasi, mime="application/pdf")
    else:
        st.warning("Önce 'Belgelerim' kısmından seçim yapın!")

elif secim == "Maliyet & Uyarı":
    st.title("⚠️ Maliyet ve Yasal Uyarı")
    if 'ulke' in st.session_state:
        ulke = st.session_state.ulke
        data = ulke_verileri[ulke]
        st.write(f"**Ülke:** {ulke}")
        st.write(f"**Vize Harcı:** {data['harc']}€ | **Servis:** {data['servis']}€")
        st.write(f"**Ekstralar:** {data['ekstra']}")
        st.warning("Yalan beyan vize yasağına yol açar.")
    else:
        st.warning("Henüz bir ülke seçilmedi.")