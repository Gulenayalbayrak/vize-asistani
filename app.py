import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Veri Tabanı (Ülke Sayısı Artırıldı)
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

# Dil Seçenekleri ve Metinler
dil_secenegi = st.sidebar.selectbox("Dil / Language:", ["Türkçe", "English"])
texts = {
    "Türkçe": {"başlık": "Vize Uzmanı", "seç": "Ülke Seçiniz:", "analiz": "Analize Git", "uyarı": "Vize Ücretleri ve Detaylar için Tıklayınız"},
    "English": {"başlık": "Visa Expert", "seç": "Select Country:", "analiz": "Go to Analysis", "uyarı": "Click for Visa Fees and Details"}
}
txt = texts[dil_secenegi]

st.title(f"🌍 {txt['başlık']}")

# Session State Yönetimi
if 'sayfa' not in st.session_state: st.session_state.sayfa = "Giriş"
if 'ulke' not in st.session_state: st.session_state.ulke = "Almanya"

# --- SAYFALAR ---
# 1. Giriş ve Belge Seçimi
if st.session_state.sayfa == "Giriş":
    ulke = st.selectbox(txt['seç'], list(ulke_verileri.keys()))
    st.session_state.ulke = ulke
    
    st.write("Belgelerinizi işaretleyin:")
    evraklar = ["Pasaport", "Sigorta", "Uçak", "Otel", "Banka", "Maaş"]
    secilenler = [e for e in evraklar if st.checkbox(e)]
    
    if st.button(txt['analiz']):
        st.session_state.secilenler = secilenler
        st.session_state.sayfa = "Analiz"
        st.rerun()

# 2. Analiz Sayfası
elif st.session_state.sayfa == "Analiz":
    ulke = st.session_state.ulke
    ihtimal = min(ulke_verileri[ulke]["onay"] + (len(st.session_state.get('secilenler', [])) * 2), 99)
    
    st.metric("Vize Onay İhtimali", f"%{ihtimal}")
    
    if ihtimal > 90:
        st.success("Vize alma olasılığınız oldukça yüksek!")
        if st.button(txt['uyarı']):
            st.session_state.sayfa = "Detay"
            st.rerun()
    else:
        st.info("Başvurunuz inceleniyor.")
        
    if st.button("Geri Dön"):
        st.session_state.sayfa = "Giriş"
        st.rerun()

# 3. Detay ve Ücretler
elif st.session_state.sayfa == "Detay":
    ulke = st.session_state.ulke
    data = ulke_verileri[ulke]
    st.subheader(f"{ulke} - Vize Ücret Bilgileri")
    st.write(f"Vize Harcı: {data['harc']}€ | Servis Bedeli: {data['servis']}€")
    st.write("Dikkat etmeniz gerekenler: Pasaport sürenizin 6 ay geçerli olduğundan emin olun.")
    
    if st.button("Ana Sayfaya Dön"):
        st.session_state.sayfa = "Giriş"
        st.rerun()