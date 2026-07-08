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

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# ZENGİN VERİ TABANI
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 25€"},
    "İspanya": {"onay": 82, "harc": 90, "servis": 30, "ekstra": "Ekspres Fark: 40€, Sigorta: 20€"},
    "İtalya": {"onay": 78, "harc": 80, "servis": 30, "ekstra": "Randevu Ücreti: 20€, Sigorta: 25€"},
    "Fransa": {"onay": 75, "harc": 80, "servis": 30, "ekstra": "Kargo: 15€, Sigorta: 20€"},
    "Hollanda": {"onay": 88, "harc": 90, "servis": 30, "ekstra": "Sigorta: 25€"},
    "Yunanistan": {"onay": 92, "harc": 80, "servis": 30, "ekstra": "Sigorta: 20€"},
    "Avusturya": {"onay": 80, "harc": 90, "servis": 30, "ekstra": "Sigorta: 22€"},
    "Çekya": {"onay": 76, "harc": 80, "servis": 30, "ekstra": "Sigorta: 18€"}
}

tum_evraklar = [
    "Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu", "Otel Rezervasyonu", 
    "Banka Hesap Dökümü", "Maaş Bordrosu", "Tapu Fotokopisi", "Araç Ruhsatı",
    "İşyeri İzin Belgesi", "Vergi Levhası", "Davetiye", "Fotoğraf", 
    "Adli Sicil Kaydı", "Nüfus Kayıt Örneği", "Diploma"
]
ZORUNLU = ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu"]

# YÖNLENDİRME MENÜSÜ
st.sidebar.title("🌍 Vize Uzmanı Menü")
secim = st.sidebar.radio("Sayfalar:", ["Hoş Geldiniz", "Belgelerim", "Analiz", "Maliyet & Uyarı"])

if secim == "Hoş Geldiniz":
    st.title("✈️ Vize Uzmanı'na Hoş Geldiniz")
    st.write("Profesyonel vize danışmanınızla tanışın. Belgelerinizi hazırlayın, onay ihtimalinizi ölçün.")

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
            st.error("❌ Eksik zorunlu belgeler: " + ", ".join([b for b in ZORUNLU if b not in secilenler]))
        else:
            st.session_state.secilenler = secilenler
            st.success("Analize yönlendiriliyorsunuz...")
            st.session_state.secim = "Analiz"
            st.rerun() # Otomatik geçiş burada çalışıyor!

elif secim == "Analiz":
    st.title("📊 Analiz Sonucu")
    if 'secilenler' in st.session_state:
        ulke = st.session_state.ulke
        ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.secilenler) * 1.5), 98)
        st.metric("Tahmini Onay İhtimali", f"%{round(ihtimal, 1)}")
        st.progress(ihtimal/100)
        if st.button("Raporu İndir"):
            pdf_dosyasi = pdf_olustur(ulke, st.session_state.secilenler, round(ihtimal, 1), ulke_verileri[ulke])
            with open(pdf_dosyasi, "rb") as f:
                st.download_button("PDF İndir", f, file_name=pdf_dosyasi, mime="application/pdf")
    else:
        st.warning("Önce 'Belgelerim' sekmesinden seçim yapın!")

elif secim == "Maliyet & Uyarı":
    st.title("⚠️ Maliyet ve Konaklama Rehberi")
    if 'ulke' in st.session_state:
        ulke = st.session_state.ulke
        data = ulke_verileri[ulke]
        st.write(f"**Ülke:** {ulke}")
        st.write(f"**Vize Harcı:** {data['harc']}€ | **Ekstralar:** {data['ekstra']}")
        st.write("---")
        st.subheader("💰 Ekonomik Konaklama (Ucuzdan Pahalıya)")
        st.markdown("""
        1. **Hosteller:** En ekonomik seçenek (Ort. 20-30€/gece).
        2. **Öğrenci Yurtları:** Sezonluk uygun fiyatlar.
        3. **Airbnb (Paylaşımlı Oda):** Yerel yaşam ve uygun fiyat.
        4. **Bütçe Otelleri:** Kahvaltı dahil (Ort. 60-80€/gece).
        """)
    else:
        st.warning("Henüz bir ülke seçilmedi.")