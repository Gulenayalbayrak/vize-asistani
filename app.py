import streamlit as st
import pandas as pd
from fpdf import FPDF

# PDF oluşturma fonksiyonu (Türkçe karakter destekli)
def pdf_olustur(ulke, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    # Türkçe karakterleri latin-1'e zorlayarak kodluyoruz
    baslik = f"{ulke} Vize Bilgilendirme Formu".encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(200, 10, txt=baslik, ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Vize Harci: {data['harc']} Euro", ln=True)
    pdf.cell(200, 10, txt=f"Sigorta: {data['sigorta']} Euro", ln=True)
    pdf.cell(200, 10, txt=f"Servis Bedeli: {data['servis']} Euro", ln=True)
    toplam = sum([data['harc'], data['sigorta'], data['servis']])
    pdf.cell(200, 10, txt=f"Toplam Tahmini: {toplam} Euro", ln=True)
    
    file_name = "vize_raporu.pdf"
    pdf.output(file_name)
    return file_name

# Sayfa Yapılandırması
st.set_page_config(page_title="Vize Uzmanı Pro", page_icon="✈️", layout="wide")

# 1. VERİTABANI
ulke_verileri = {
    "Almanya": {"evraklar": ["Pasaport", "Sigorta", "Uçak"], "harc": 90, "sigorta": 25, "servis": 30, "onay": 85},
    "Ispanya": {"evraklar": ["Pasaport", "Otel", "Banka"], "harc": 90, "sigorta": 20, "servis": 30, "onay": 82},
    "Italya": {"evraklar": ["Davet", "Sigorta", "Gelir"], "harc": 80, "sigorta": 25, "servis": 30, "onay": 78},
    "Fransa": {"evraklar": ["Banka", "Uçak", "Otel"], "harc": 80, "sigorta": 20, "servis": 30, "onay": 75},
    "Hollanda": {"evraklar": ["Sigorta", "Maas", "Pasaport"], "harc": 90, "sigorta": 25, "servis": 30, "onay": 88},
    "Belcika": {"evraklar": ["Pasaport", "Foto", "Sigorta"], "harc": 90, "sigorta": 20, "servis": 30, "onay": 70},
    "Yunanistan": {"evraklar": ["Otel", "Uçak", "Sigorta"], "harc": 80, "sigorta": 20, "servis": 30, "onay": 92}
}

# 2. SIDEBAR
st.sidebar.title("Menu")
ulke = st.sidebar.selectbox("Ulke Seciniz:", ["Seciniz..."] + list(ulke_verileri.keys()))

# 3. ANA EKRAN
if ulke == "Seciniz...":
    st.title("✈️ Avrupa Vize ve Seyahat Portali")
    st.info("Ulkelerin vize onay istatistiklerini asagidan inceleyebilirsiniz.")
    
    df = pd.DataFrame.from_dict(ulke_verileri, orient='index')
    st.subheader("📊 Ulke Bazli Vize Onay Oranlari (%)")
    st.bar_chart(df["onay"])
    
    st.write("---")
    st.subheader("Sistem Istatistikleri")
    col1, col2 = st.columns(2)
    col1.metric("Desteklenen Ulke", len(ulke_verileri))
    col2.metric("Ortalama Onay Orani", f"{round(df['onay'].mean(), 1)}%")

else:
    data = ulke_verileri[ulke]
    st.title(f"🌍 {ulke} Vize Asistani")
    
    t1, t2 = st.tabs(["📄 Gerekli Evraklar", "💰 Maliyet Analizi"])
    with t1:
        st.subheader("Gerekli Evrak Listesi")
        for doc in data["evraklar"]:
            st.checkbox(doc)
            
    with t2:
        st.subheader("Tahmini Maliyet Hesaplama")
        st.table({"Kalem": ["Vize Harci", "Sigorta", "Servis"], "Tutar (€)": [data["harc"], data["sigorta"], data["servis"]]})
        toplam = sum([data['harc'], data['sigorta'], data['servis']])
        st.metric("Toplam Tahmini", f"{toplam} €")
        
        st.write(f"Vize Onay Ihtimali: %{data['onay']}")
        st.progress(data["onay"]/100)
        
        pdf_dosyasi = pdf_olustur(ulke, data)
        with open(pdf_dosyasi, "rb") as f:
            st.download_button("📄 PDF Olarak Indir", f, file_name=pdf_dosyasi, mime="application/pdf")