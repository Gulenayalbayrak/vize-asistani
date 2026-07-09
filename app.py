import streamlit as st

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Dil Seçeneği (Daha şık ve ferah)
st.markdown("---")
col_dil1, col_dil2 = st.columns([8, 2])
with col_dil2:
    dil = st.selectbox("🌐 Dil Seçiniz:", ["Türkçe", "English"])
st.markdown("---")

txt = {
    "Türkçe": {"başlık": "Vize Uzmanı Portalı", "başla": "Başvuruyu Başlat", "seçim": "Belgeler ve Risk", "analiz": "Analize Git", "sonuç": "Analiz Sonucu", "detay": "Detaylar ve Randevu", "neden": "Not: Vize ihtimaliniz şu sebeplerle düşük çıkmış olabilir:"},
    "English": {"başlık": "Visa Expert Portal", "başla": "Start Application", "seçim": "Documents & Risk", "analiz": "Go to Analysis", "sonuç": "Analysis Result", "detay": "Details & Appointment", "neden": "Note: Your visa probability might be low due to the following reasons:"}
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
        st.session_state.aktif_riskler = [soru for soru, puan in risk_sorulari.items() if st.checkbox(soru, key=f"check_{soru}")]
        
    if st.button(txt['analiz']):
        st.session_state.sayfa = "Analiz"
        st.rerun()

elif st.session_state.sayfa == "Analiz":
    st.title(f"📊 {txt['sonuç']}")
    ihtimal = min(ulke_verileri[st.session_state.ulke]["onay"] + (len(st.session_state.secilenler) * 2) - st.session_state.risk_puani, 99)
    st.metric("Onay İhtimali", f"%{max(ihtimal, 5)}")
    
    if ihtimal < 80:
        st.write(f"**{txt['neden']}**")
        for risk in st.session_state.aktif_riskler: st.error(f"- {risk}")
        
    if st.button(txt['detay']):
        st.session_state.sayfa = "Detay"
        st.rerun()

elif st.session_state.sayfa == "Detay":
    st.title(f"💡 {txt['detay']}")
    data = ulke_verileri[st.session_state.ulke]
    st.write(f"### 💶 Vize Ücretleri")
    st.write(f"Vize Harcı: {data['harc']}€ | Servis Bedeli: {data['servis']}€")
    st.write("### 📝 Randevu ve Başvuru Stratejileri")
    st.markdown("""
    1. **Randevu Takibi:** Konsoloslukların randevu sistemleri genellikle gece 00:00 ile 02:00 arasında güncellenir.
    2. **Finansal Hazırlık:** Banka dökümünüzde son 3 aya ait hareketlerin istikrarlı olduğundan emin olun.
    3. **Belge Kalitesi:** Tüm belgelerin fotokopilerini ve asıllarını ayrı ayrı dosyalayın.
    4. **İkametgah:** İkamet ettiğiniz ile bakan yetkili aracı kurumu mutlaka doğru seçin.
    5. **Seyahat Planı:** Uçak ve otel rezervasyonlarınızın 'gerçek' ve 'teyit edilebilir' olduğundan emin olun.
    """)
    if st.button("Ana Sayfa"):
        st.session_state.sayfa = "Giriş"
        st.rerun()