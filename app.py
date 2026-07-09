import streamlit as st

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# GENİŞLETİLMİŞ VERİ TABANI
ulke_verileri = {
    "Almanya": {"onay": 85, "harc": 90, "servis": 30},
    "İspanya": {"onay": 82, "harc": 90, "servis": 30},
    "İtalya": {"onay": 78, "harc": 80, "servis": 30},
    "Fransa": {"onay": 75, "harc": 80, "servis": 30},
    "Hollanda": {"onay": 88, "harc": 90, "servis": 30},
    "Yunanistan": {"onay": 92, "harc": 80, "servis": 30},
    "Avusturya": {"onay": 80, "harc": 90, "servis": 30},
    "Belçika": {"onay": 70, "harc": 90, "servis": 30},
    "İsveç": {"onay": 83, "harc": 90, "servis": 30},
    "İsviçre": {"onay": 86, "harc": 95, "servis": 30}
}

tum_evraklar = [
    "Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu", "Otel Rezervasyonu", 
    "Banka Hesap Dökümü", "Maaş Bordrosu", "Tapu Fotokopisi", "Araç Ruhsatı",
    "İşyeri İzin Belgesi", "Vergi Levhası", "Davetiye", "Fotoğraf", 
    "Adli Sicil Kaydı", "Nüfus Kayıt Örneği", "Diploma"
]

risk_sorulari = {
    "Daha önce vize reddi aldınız mı?": 20,
    "Bankada düzenli geliriniz yok mu?": 25,
    "Pasaport süreniz 6 aydan kısa mı?": 30
}

# DİL VE AKIŞ YÖNETİMİ
dil = st.sidebar.selectbox("Language / Dil:", ["Türkçe", "English"])
txt = {
    "Türkçe": {"başlık": "Vize Uzmanı", "seçim": "Belgeler ve Risk", "analiz": "Analiz", "detay": "Detaylar"},
    "English": {"başlık": "Visa Expert", "seçim": "Documents & Risk", "analiz": "Analysis", "detay": "Details"}
}[dil]

if 'sayfa' not in st.session_state: st.session_state.sayfa = "Giriş"
secim = st.sidebar.radio("Navigasyon", ["Giriş", txt['seçim'], txt['analiz'], txt['detay']])
st.session_state.sayfa = secim

# --- SAYFALAR ---
if st.session_state.sayfa == "Giriş":
    st.title(f"✈️ {txt['başlık']}")
    st.write("Vize başvurularınız için profesyonel destek.")

elif st.session_state.sayfa == txt['seçim']:
    st.title(f"📄 {txt['seçim']}")
    st.session_state.ulke = st.selectbox("Ülke:", list(ulke_verileri.keys()))
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Gerekli Belgeler")
        st.session_state.secilenler = [e for e in tum_evraklar if st.checkbox(e, key=e)]
    with col2:
        st.subheader("⚠️ Risk Soruları")
        st.session_state.risk_puani = sum([puan for soru, puan in risk_sorulari.items() if st.checkbox(soru)])
    
    if st.button("Analize Git"):
        st.session_state.sayfa = txt['analiz']
        st.rerun()

elif st.session_state.sayfa == txt['analiz']:
    st.title(f"📊 {txt['analiz']}")
    ulke = st.session_state.get('ulke', 'Almanya')
    ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.get('secilenler', [])) * 1.5) - st.session_state.get('risk_puani', 0), 99)
    st.metric("Onay İhtimali", f"%{max(ihtimal, 5)}")
    
    if ihtimal < 50: st.error("İhtimal düşük! Eksikleri giderin.")
    else: st.success("İhtimal iyi.")
    
    if st.button("Randevu ve Detaylar"):
        st.session_state.sayfa = txt['detay']
        st.rerun()

elif st.session_state.sayfa == txt['detay']:
    st.title(f"💡 {txt['detay']}")
    data = ulke_verileri[st.session_state.get('ulke', 'Almanya')]
    st.write(f"Vize Harcı: {data['harc']}€ | Servis: {data['servis']}€")
    st.markdown("""
    **Randevu İpuçları:**
    * Randevu sistemlerini gece 00:00 - 02:00 arası kontrol edin.
    * Bölgesel başvuru merkezini doğru seçtiğinizden emin olun.
    * Belgelerinizin orijinali ve fotokopilerini dosya halinde hazır bulundurun.
    """)