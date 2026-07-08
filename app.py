import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF Fonksiyonu (Hata payını sıfıra indiren basit yapı)
def pdf_olustur(ulke, secilenler, ihtimal, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"{ulke} Vize Raporu", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Onay Ihtimali: %{ihtimal}", ln=True)
    for doc in secilenler:
        pdf.cell(200, 10, txt=f"- {doc}", ln=True)
    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(layout="wide")

# Veri Tabanı
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 25€"},
    "İspanya": {"onay": 82, "harc": 90, "servis": 30, "ekstra": "Ekspres Fark: 40€, Sigorta: 20€"},
    "İtalya": {"onay": 78, "harc": 80, "servis": 30, "ekstra": "Randevu Ücreti: 20€, Sigorta: 25€"}
}
tum_evraklar = ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu", "Otel Rezervasyonu", "Banka Hesap Dökümü", "Maaş Bordrosu"]
ZORUNLU = ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu"]

# Yönlendirme Kontrolü
if 'sayfa' not in st.session_state: st.session_state.sayfa = "Hoş Geldiniz"

# Yan Menü
secim = st.sidebar.radio("Navigasyon:", ["Hoş Geldiniz", "Belgelerim", "Analiz", "Maliyet & Uyarı"], 
                         index=["Hoş Geldiniz", "Belgelerim", "Analiz", "Maliyet & Uyarı"].index(st.session_state.sayfa))
st.session_state.sayfa = secim

# Sayfa İçerikleri
if secim == "Hoş Geldiniz":
    st.title("Vize Uzmanı Portalı")
    st.write("Başlamak için yan menüyü kullanın.")

elif secim == "Belgelerim":
    st.title("📄 Belgelerim")
    ulke = st.selectbox("Ülke:", list(ulke_verileri.keys()))
    st.session_state.ulke = ulke
    
    secilenler = [e for e in tum_evraklar if st.checkbox(e, key=e)]
    
    if st.button("Analize Git"):
        if any(z not in secilenler for z in ZORUNLU):
            st.error("Zorunlu belgeler eksik!")
        else:
            st.session_state.secilenler = secilenler
            st.session_state.sayfa = "Analiz"
            st.rerun()

elif secim == "Analiz":
    st.title("📊 Analiz Sonucu")
    if 'secilenler' in st.session_state:
        ulke = st.session_state.ulke
        ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.secilenler) * 2), 98)
        st.metric("Tahmini Onay", f"%{ihtimal}")
        
        # PDF İndirme (Dosya oluşturma hatasını engellemek için doğrudan buton)
        pdf_data = pdf_olustur(ulke, st.session_state.secilenler, ihtimal, ulke_verileri[ulke])
        st.download_button("PDF İndir", pdf_data, "rapor.pdf", "application/pdf")
    else:
        st.warning("Önce belgeleri seçin!")