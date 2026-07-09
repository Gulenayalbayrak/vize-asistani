import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Veri Tabanı
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

# Dil Seçenekleri
dil = st.sidebar.selectbox("Language / Dil:", ["Türkçe", "English"])
txt = {
    "Türkçe": {"başlık": "Vize Uzmanı", "giriş": "Hoş Geldiniz", "başla": "Başvuruyu Başlat", "detay": "Detaylar için Tıklayınız", "randevu": "Randevu İpuçları"},
    "English": {"başlık": "Visa Expert", "giriş": "Welcome", "başla": "Start Application", "detay": "Click for Details", "randevu": "Appointment Tips"}
}[dil]

# Session State
if 'sayfa' not in st.session_state: st.session_state.sayfa = "Giriş"

# --- SAYFA AKIŞI ---

if st.session_state.sayfa == "Giriş":
    st.title(f"✈️ {txt['başlık']}")
    st.write(f"## {txt['giriş']}")
    st.write("Vize başvurularınızda doğru analiz için hazır mısınız?")
    if st.button(txt['başla']):
        st.session_state.sayfa = "Seçim"
        st.rerun()

elif st.session_state.sayfa == "Seçim":
    ulke = st.selectbox("Ülke Seçiniz:", list(ulke_verileri.keys()))
    st.session_state.ulke = ulke
    
    st.write("Belgelerinizi işaretleyin:")
    secilenler = [e for e in ["Pasaport", "Sigorta", "Uçak", "Otel", "Banka"] if st.checkbox(e)]
    
    if st.button("Analiz Et"):
        st.session_state.secilenler = secilenler
        st.session_state.sayfa = "Analiz"
        st.rerun()

elif st.session_state.sayfa == "Analiz":
    ulke = st.session_state.ulke
    ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.get('secilenler', [])) * 2), 99)
    st.metric("Onay İhtimali", f"%{ihtimal}")
    
    if ihtimal > 80:
        if st.button(txt['detay']):
            st.session_state.sayfa = "Detay"
            st.rerun()
    
    if st.button("Geri"):
        st.session_state.sayfa = "Seçim"
        st.rerun()

elif st.session_state.sayfa == "Detay":
    ulke = st.session_state.ulke
    data = ulke_verileri[ulke]
    st.subheader(f"{ulke} - Bilgilendirme")
    st.write(f"Vize Harcı: {data['harc']}€ | Servis Bedeli: {data['servis']}€")
    
    st.subheader(f"💡 {txt['randevu']}")
    st.markdown("""
    * **Erken Randevu:** Randevu sistemleri genellikle gece yarısı güncellenir.
    * **Doğru Vize Türü:** Turistik yerine ticari vize seçmek randevu yoğunluğunu değiştirebilir.
    * **Bölgesel Başvuru:** İkamet ettiğiniz şehre bakan konsolosluk birimini doğru seçin.
    * **Sürekli Kontrol:** İptal olan randevuları yakalamak için günde en az 3 kez giriş yapın.
    """)
    
    if st.button("Ana Sayfa"):
        st.session_state.sayfa = "Giriş"
        st.rerun()