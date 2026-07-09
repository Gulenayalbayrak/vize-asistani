import streamlit as st

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Dil Seçeneği (Sağ üst, sıkışık değil)
st.markdown("---")
col_dil1, col_dil2 = st.columns([8, 2])
with col_dil2:
    dil = st.selectbox("🌐 Dil Seçiniz / Select Language / اختر اللغة:", ["Türkçe", "English", "العربية"])
st.markdown("---")

txt = {
    "Türkçe": {
        "başlık": "Vize Uzmanı Portalı", "başla": "Başvuruyu Başlat", "seçim": "Belgeler ve Risk", 
        "analiz": "Analize Git", "sonuç": "Analiz Sonucu", "detay": "Detaylar ve Randevu",
        "uyarı": "Vize alma olasılığınız aşağıdaki sebeplerden dolayı düşüktür. İşleminize devam etmeden önce bunları düzeltmeniz gerekir:",
        "çözümler": {
            "Daha önce vize reddi aldınız mı?": "Önceki vize reddinizin gerekçesini açıklayan bir ön yazı (cover letter) hazırlayın.",
            "Düzenli geliriniz yok mu?": "Banka hesabınıza düzenli giriş-çıkış sağlayacak ek bir gelir kaynağı veya sponsor belgesi ekleyin.",
            "Pasaport süresi 6 aydan az mı?": "Pasaportunuzu yenileyin; vize işlemleri için en az 6 ay geçerlilik şarttır."
        }
    },
    "English": {
        "başlık": "Visa Expert Portal", "başla": "Start Application", "seçim": "Documents & Risk", 
        "analiz": "Go to Analysis", "sonuç": "Analysis Result", "detay": "Details & Appointment",
        "uyarı": "Your visa probability is low due to the following reasons. You must fix these before proceeding:",
        "çözümler": {
            "Daha önce vize reddi aldınız mı?": "Prepare a cover letter explaining the reason for your previous visa refusal.",
            "Düzenli geliriniz yok mu?": "Provide proof of additional income or a sponsor document.",
            "Pasaport süresi 6 aydan az mı?": "Renew your passport; it must be valid for at least 6 months."
        }
    },
    "العربية": {
        "başlık": "بوابة خبير التأشيرات", "başla": "ابدأ الطلب", "seçim": "المستندات والمخاطر", 
        "analiz": "اذهب إلى التحليل", "sonuç": "نتيجة التحليل", "detay": "التفاصيل والموعد",
        "uyarı": "احتمالية الحصول على التأشيرة منخفضة للأسباب التالية. نوصي بإصلاح هذه المشكلات قبل المتابعة:",
        "çözümler": {
            "Daha önce vize reddi aldınız mı?": "قم بإعداد خطاب يوضح سبب رفض التأشيرة السابق.",
            "Düzenli geliriniz yok mu?": "قدم إثبات دخل إضافي أو مستند كفيل.",
            "Pasaport süresi 6 aydan az mı?": "قم بتجديد جواز سفرك؛ يجب أن يكون صالحًا لمدة 6 أشهر على الأقل."
        }
    }
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
risk_tanimlari = {"Daha önce vize reddi aldınız mı?": 20, "Düzenli geliriniz yok mu?": 25, "Pasaport süresi 6 aydan az mı?": 30}

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
        st.session_state.aktif_riskler = [soru for soru in risk_tanimlari.keys() if st.checkbox(soru, key=f"check_{soru}")]
        st.session_state.risk_puani = sum([risk_tanimlari[s] for s in st.session_state.aktif_riskler])
        
    if st.button(txt['analiz']):
        st.session_state.sayfa = "Analiz"
        st.rerun()

elif st.session_state.sayfa == "Analiz":
    st.title(f"📊 {txt['sonuç']}")
    ihtimal = min(ulke_verileri[st.session_state.ulke]["onay"] + (len(st.session_state.secilenler) * 2) - st.session_state.risk_puani, 99)
    st.metric("Onay İhtimali", f"%{max(ihtimal, 5)}")
    
    if ihtimal < 80:
        st.warning(txt['uyarı'])
        for risk in st.session_state.get('aktif_riskler', []):
            st.error(f"❌ {risk} -> **{txt['çözümler'][risk]}**")
        
    if st.button(txt['detay']):
        st.session_state.sayfa = "Detay"
        st.rerun()

elif st.session_state.sayfa == "Detay":
    st.title(f"💡 {txt['detay']}")
    data = ulke_verileri[st.session_state.ulke]
    st.write(f"### 💶 Vize Ücretleri")
    st.write(f"Vize Harcı: {data['harc']}€ | Servis Bedeli: {data['servis']}€")
    st.markdown("### 📝 Randevu ve Başvuru Stratejileri")
    st.markdown