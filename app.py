import streamlit as st

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Veri Tabanı
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30},
    "İspanya": {"onay": 82, "harc": 90, "servis": 30},
    "İtalya": {"onay": 78, "harc": 80, "servis": 30}
}

risk_sorulari = {
    "Daha önce vize reddi aldınız mı?": 20,
    "Bankada düzenli geliriniz yok mu?": 25,
    "Pasaport süreniz 6 aydan kısa mı?": 30
}

# Session State
if 'sayfa' not in st.session_state: st.session_state.sayfa = "Giriş"

# Menü
secim = st.sidebar.radio("Navigasyon", ["Giriş", "Seçim", "Analiz", "Detay"])
st.session_state.sayfa = secim

if st.session_state.sayfa == "Giriş":
    st.title("✈️ Vize Uzmanı")
    st.write("Hoş geldiniz! Başvuruyu başlatmak için yan menüden 'Seçim'e geçin.")

elif st.session_state.sayfa == "Seçim":
    ulke = st.selectbox("Ülke:", list(ulke_verileri.keys()))
    st.session_state.ulke = ulke
    st.write("### Risk Kontrolü:")
    st.session_state.risk_puani = sum([puan for soru, puan in risk_sorulari.items() if st.checkbox(soru)])
    if st.button("Analiz Et"):
        st.session_state.sayfa = "Analiz"
        st.rerun()

elif st.session_state.sayfa == "Analiz":
    ulke = st.session_state.ulke
    ihtimal = max(ulke_verileri[ulke]["onay"] - st.session_state.get('risk_puani', 0), 5)
    st.metric("Vize İhtimali", f"%{ihtimal}")
    if ihtimal < 50:
        st.error("İhtimal düşük! Eksikleri giderin.")
    else:
        st.success("İhtimal iyi.")
        if st.button("Detayları Gör"):
            st.session_state.sayfa = "Detay"
            st.rerun()

elif st.session_state.sayfa == "Detay":
    st.write("Vize ücretleri ve randevu ipuçları burada yer alacak.")