import streamlit as st
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(page_title="Vize Uzmanı Pro", page_icon="✈️", layout="wide")

# 1. VERİTABANI
ulke_verileri = {
    "Almanya": {"evraklar": ["Pasaport", "Sigorta", "Uçak"], "harc": 90, "sigorta": 25, "servis": 30, "onay": 85},
    "İspanya": {"evraklar": ["Pasaport", "Otel", "Banka"], "harc": 90, "sigorta": 20, "servis": 30, "onay": 82},
    "İtalya": {"evraklar": ["Davet", "Sigorta", "Gelir"], "harc": 80, "sigorta": 25, "servis": 30, "onay": 78},
    "Fransa": {"evraklar": ["Banka", "Uçak", "Otel"], "harc": 80, "sigorta": 20, "servis": 30, "onay": 75},
    "Hollanda": {"evraklar": ["Sigorta", "Maaş", "Pasaport"], "harc": 90, "sigorta": 25, "servis": 30, "onay": 88},
    "Belçika": {"evraklar": ["Pasaport", "Foto", "Sigorta"], "harc": 90, "sigorta": 20, "servis": 30, "onay": 70},
    "Yunanistan": {"evraklar": ["Otel", "Uçak", "Sigorta"], "harc": 80, "sigorta": 20, "servis": 30, "onay": 92}
}

# 2. SIDEBAR
st.sidebar.title("Menü")
ulke = st.sidebar.selectbox("Ülke Seçiniz:", ["Seçiniz..."] + list(ulke_verileri.keys()))

# 3. ANA EKRAN
if ulke == "Seçiniz...":
    st.title("✈️ Avrupa Vize ve Seyahat Portalı")
    st.info("Ülkelerin vize onay istatistiklerini aşağıdan inceleyebilirsiniz.")
    
    # Onay Grafiği için veri hazırlama
    df = pd.DataFrame.from_dict(ulke_verileri, orient='index')
    st.subheader("📊 Ülke Bazlı Vize Onay Oranları (%)")
    st.bar_chart(df["onay"])
    
    st.write("---")
    st.subheader("Sistem İstatistikleri")
    col1, col2 = st.columns(2)
    col1.metric("Desteklenen Ülke", len(ulke_verileri))
    col2.metric("Ortalama Onay Oranı", f"{round(df['onay'].mean(), 1)}%")

else:
    # SEÇİM SONRASI DETAYLAR
    data = ulke_verileri[ulke]
    st.title(f"🌍 {ulke} Vize Asistanı")
    
    t1, t2 = st.tabs(["📄 Gerekli Evraklar", "💰 Maliyet Analizi"])
    with t1:
        st.subheader("Gerekli Evrak Listesi")
        for doc in data["evraklar"]:
            st.checkbox(doc)
    with t2:
        st.subheader("Tahmini Maliyet Hesaplama")
        st.table({"Kalem": ["Vize Harcı", "Sigorta", "Servis"], "Tutar (€)": [data["harc"], data["sigorta"], data["servis"]]})
        toplam = sum([data['harc'], data['sigorta'], data['servis']])
        st.metric("Toplam Tahmini", f"{toplam} €")
        
        st.write(f"Vize Onay İhtimali: %{data['onay']}")
        st.progress(data["onay"]/100)