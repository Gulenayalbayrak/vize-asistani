import streamlit as st

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Dil Seçeneği Sağ Üst Köşe
col_dil, _ = st.columns([1, 9])
with col_dil:
    dil = st.selectbox("Language", ["Türkçe", "English"], label_visibility="collapsed")

txt = {
    "Türkçe": {"başlık": "Vize Uzmanı Portalı", "başla": "Başvuruyu Başlat", "seçim": "Belgeler ve Risk", "analiz": "Analize Git", "sonuç": "Analiz Sonucu", "detay": "Detaylar ve Randevu"},
    "English": {"başlık": "Visa Expert Portal", "başla": "Start Application", "seçim": "Documents & Risk", "analiz": "Go to Analysis", "sonuç": "Analysis Result", "detay": "Details & Appointment"}
}[dil]

# Veri Tabanı
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30}, "İspanya": {"onay": 82, "harc": 90, "servis": 30},
    "İtalya": {"onay": 78, "harc": 80, "servis": 30}, "Fransa": {"onay": 75, "harc": 80, "servis": 30},
    "Hollanda": {"onay": 88, "harc": 90, "servis": 30}, "Yunanistan": {"onay": 92, "harc": 80, "servis": 30},
    "Avusturya": {"onay": 80, "harc": 90, "servis": 30}, "Belçika": {"onay": 70, "harc": 90, "servis": 30},
    "İsveç": {"onay": 83, "harc": 90, "servis": 30}, "İsviçre": {"onay": 86, "harc": 95, "servis": 30}
}
tum_evraklar = ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu", "Otel Rezervasyonu", "Banka Hesap Dökümü", "Maaş Bordrosu", "Tapu", "Araç", "Davetiye"]
risk_sorulari = {"Daha önce vize reddi aldınız mı?": 20, "Düzenli geliriniz yok mu?": 25, "Pasaport süresi 6 aydan az mı?": 30}

# Sayfa Yönetimi
if 'sayfa' not in st.session_state: st.session_state.sayfa = "Giriş"

# --- EKRANLAR ---
if st.session_state.sayfa == "Giriş":
    st.title(f"✈️ {txt['başlık']}")
    if st.button(txt['başla']):
        st.session_state.sayfa = "Seçim"
        st.rerun()

elif st.session_state.sayfa == "Seçim":
    st.title(f"📄 {txt['seçim']}")
    st.session_state.ulke = st.selectbox("Ülke:", list(ulke_verileri.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.secilenler = [e for e in tum_evraklar if st.checkbox(e, key=e)]
    with col2:
        st.session_state.risk_puani = sum([puan for soru, puan in risk_sorulari.items() if st.checkbox(soru)])
        
    if st.button(txt['analiz']):
        st.session_state.sayfa = "Analiz"
        st.rerun()

elif st.session_state.sayfa == "Analiz":
    st.title(f"📊 {txt['sonuç']}")
    ihtimal = min(ulke_verileri[st.session_state.ulke]["onay"] + (len(st.session_state.secilenler) * 2) - st.session_state.risk_puani, 99)
    st.metric("Onay İhtimali", f"%{max(ihtimal, 5)}")
    
    if st.button(txt['detay']):
        st.session_state.sayfa = "Detay"
        st.rerun()

elif st.session_state.sayfa == "Detay":
    st.title(f"💡 {txt['detay']}")
    data = ulke_verileri[st.session_state.ulke]
    st.write(f"Vize Harcı: {data['harc']}€ | Servis: {data['servis']}€")
    st.markdown("**Randevu İpuçları:**\n* Gece 00:00-02:00 arası kontrol edin.\n* Bölgesel birimleri doğru seçin.")
    if st.button("Ana Sayfa"):
        st.session_state.sayfa = "Giriş"
        st.rerun()