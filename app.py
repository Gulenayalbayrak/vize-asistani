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
    pdf.cell(200, 10, txt=f"Onay İhtimali: %{ihtimal}", ln=True)
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

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# GENİŞLETİLMİŞ VERİ TABANI
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 25€"},
    "İspanya": {"onay": 82, "harc": 90, "servis": 30, "ekstra": "Ekspres Fark: 40€, Sigorta: 20€"},
    "İtalya": {"onay": 78, "harc": 80, "servis": 30, "ekstra": "Randevu Ücreti: 20€, Sigorta: 25€"},
    "Fransa": {"onay": 75, "harc": 80, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 20€"},
    "Hollanda": {"onay": 88, "harc": 90, "servis": 30, "ekstra": "Sigorta: 25€"},
    "Yunanistan": {"onay": 92, "harc": 80, "servis": 30, "ekstra": "Sigorta: 20€"},
    "Avusturya": {"onay": 80, "harc": 90, "servis": 30, "ekstra": "Sigorta: 22€"},
    "Çekya": {"onay": 76, "harc": 80, "servis": 30, "ekstra": "Sigorta: 18€"},
    "Belçika": {"onay": 70, "harc": 90, "servis": 30, "ekstra": "Sigorta: 20€"},
    "İsveç": {"onay": 83, "harc": 90, "servis": 30, "ekstra": "Sigorta: 25€"}
}

tum_evraklar = [
    "Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu", "Otel Rezervasyonu", 
    "Banka Hesap Dökümü", "Maaş Bordrosu", "Tapu Fotokopisi", "Araç Ruhsatı",
    "İşyeri İzin Belgesi", "Vergi Levhası", "Davetiye", "Fotoğraf", 
    "Adli Sicil Kaydı", "Nüfus Kayıt Örneği", "Diploma", "Askerlik Durum Belgesi",
    "Kredi Kartı Ekstresi", "E-Devlet Barkodlu Belge"
]
ZORUNLU = ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu"]

# YÖNLENDİRME MANTIĞI
if 'sayfa' not in st.session_state:
    st.session_state.sayfa = "Hoş Geldiniz"

# YAN MENÜ
menu = st.sidebar.radio("Menü:", ["Hoş Geldiniz", "Belgelerim", "Analiz", "Maliyet & Uyarı"], 
                        index=["Hoş Geldiniz", "Belgelerim", "Analiz", "Maliyet & Uyarı"].index(st.session_state.sayfa))
st.session_state.sayfa = menu

if menu == "Hoş Geldiniz":
    st.title("✈️ Vize Uzmanı Portalı")
    st.write("Vize süreçleriniz için profesyonel analiz merkezi.")

elif menu == "Belgelerim":
    st.title("📄 Belgelerim")
    ulke = st.selectbox("Ülke:", list(ulke_verileri.keys()))
    st.session_state.secilen_ulke = ulke
    
    secilenler = []
    cols = st.columns(3)
    for i, evrak in enumerate(tum_evraklar):
        if cols[i % 3].checkbox(evrak, key=f"cb_{evrak}"): secilenler.append(evrak)
    
    if st.button("Analize Git"):
        if [b for b in ZORUNLU if b not in secilenler]:
            st.error("Eksik zorunlu belgeler var!")
        else:
            st.session_state.secilenler = secilenler
            st.session_state.sayfa = "Analiz"
            st.rerun()

elif menu == "Analiz":
    st.title("📊 Analiz Sonucu")
    if 'secilenler' in st.session_state:
        ulke = st.session_state.secilen_ulke
        ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.secilenler) * 1.5), 98)
        st.metric("Tahmini Onay İhtimali", f"%{round(ihtimal, 1)}")
        st.progress(ihtimal/100)
        if st.button("Raporu İndir"):
            pdf_dosyasi = pdf_olustur(ulke, st.session_state.secilenler, round(ihtimal, 1), ulke_verileri[ulke])
            with open(pdf_dosyasi, "rb") as f:
                st.download_button("PDF İndir", f, file_name=pdf_dosyasi, mime="application/pdf")
    else:
        st.warning("Önce belgeleri seçin!")

elif menu == "Maliyet & Uyarı":
    st.title("⚠️ Maliyet ve Uyarı")
    if 'secilen_ulke' in st.session_state:
        data = ulke_verileri[st.session_state.secilen_ulke]
        st.write(f"**Ülke:** {st.session_state.secilen_ulke}")
        st.write(f"**Harç:** {data['harc']}€ | **Ekstralar:** {data['ekstra']}")
    else:
        st.warning("Ülke seçimi yapılmadı.")