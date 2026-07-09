import streamlit as st

st.set_page_config(page_title="Vize Uzmanı", layout="wide")

# Dil Seçeneği
st.markdown("---")
col_dil1, col_dil2 = st.columns([8, 2])
with col_dil2:
    dil = st.selectbox("🌐 Dil:", ["Türkçe", "English", "العربية"])
st.markdown("---")

txt = {
    "Türkçe": {
        "başlık": "Vize Uzmanı Portalı", "başla": "Başvuruyu Başlat", "seçim": "Belgeler ve Risk", 
        "analiz": "Analize Git", "sonuç": "Analiz Sonucu", "detay": "Detaylar ve Randevu",
        "belgeler": "Gerekli Belgeler", "risk_başlık": "⚠️ Risk Soruları",
        "ülkeler": {"Almanya": "Almanya", "İspanya": "İspanya", "İtalya": "İtalya", "Fransa": "Fransa", "Hollanda": "Hollanda"},
        "evraklar": ["Pasaport", "Sigorta Poliçesi", "Uçak Rezervasyonu", "Otel Rezervasyonu", "Banka Hesap Dökümü", "Maaş Bordrosu", "Tapu", "Araç", "Davetiye"],
        "riskler": {"Daha önce vize reddi aldınız mı?": 20, "Düzenli geliriniz yok mu?": 25, "Pasaport süresi 6 aydan az mı?": 30},
        "uyarı": "Vize alma olasılığınız aşağıdaki sebeplerden dolayı düşüktür:",
        "çözümler": {"Daha önce vize reddi aldınız mı?": "Red gerekçesini açıklayan bir ön yazı hazırlayın.", "Düzenli geliriniz yok mu?": "Ek gelir veya sponsor belgesi ekleyin.", "Pasaport süresi 6 aydan az mı?": "Pasaportunuzu yenileyin."},
        "strateji": "Detaylı Randevu Rehberi", "detay_metin": "1. Randevu takibi: Gece 00-02 arası. 2. Finansal istikrar: Son 3 ay. 3. Evrak dizilimi: Klasör düzeni önemlidir. 4. İkametgah: Yetkili merkez kontrolü. 5. Rezervasyon: Teyit edilebilir olması gerekir."
    },
    "English": {
        "başlık": "Visa Expert Portal", "başla": "Start Application", "seçim": "Documents & Risk", 
        "analiz": "Go to Analysis", "sonuç": "Analysis Result", "detay": "Details & Appointment",
        "belgeler": "Required Documents", "risk_başlık": "⚠️ Risk Factors",
        "ülkeler": {"Germany": "Germany", "Spain": "Spain", "Italy": "Italy", "France": "France", "Netherlands": "Netherlands"},
        "evraklar": ["Passport", "Insurance Policy", "Flight Reservation", "Hotel Reservation", "Bank Statement", "Salary Slip", "Deed", "Vehicle", "Invitation"],
        "riskler": {"Have you been refused a visa before?": 20, "No regular income?": 25, "Passport valid less than 6 months?": 30},
        "uyarı": "Your visa probability is low due to the following:",
        "çözümler": {"Have you been refused a visa before?": "Prepare a cover letter.", "No regular income?": "Provide proof of additional income.", "Passport valid less than 6 months?": "Renew your passport."},
        "strateji": "Detailed Appointment Guide", "detay_metin": "1. Appointment Tracking: Check between 00:00-02:00 AM. 2. Financial Stability: Last 3 months records. 3. Document Order: Keep files organized. 4. Jurisdiction: Verify embassy rules. 5. Reservation: Ensure bookings are confirmed."
    },
    "العربية": {
        "başlık": "بوابة خبير التأشيرات", "başla": "ابدأ الطلب", "seçim": "المستندات والمخاطر", 
        "analiz": "اذهب إلى التحليل", "sonuç": "نتيجة التحليل", "detay": "التفاصيل والموعد",
        "belgeler": "المستندات المطلوبة", "risk_başlık": "⚠️ عوامل الخطر",
        "ülkeler": {"ألمانيا": "ألمانيا", "إسبانيا": "إسبانيا", "إيطاليا": "إيطاليا", "فرنسا": "فرنسا", "هولندا": "هولندا"},
        "evraklar": ["جواز السفر", "بوليصة التأمين", "حجز الطيران", "حجز الفندق", "كشف حساب بنكي", "قسيمة الراتب", "سند الملكية", "مركبة", "دعوة"],
        "riskler": {"هل سبق لك رفض التأشيرة؟": 20, "لا يوجد دخل منتظم؟": 25, "صلاحية جواز السفر أقل من 6 أشهر؟": 30},
        "uyarı": "احتمالية الحصول على التأشيرة منخفضة للأسباب التالية:",
        "çözümler": {"هل سبق لك رفض التأشيرة؟": "قم بإعداد خطاب توضيحي.", "لا يوجد دخل منتظم؟": "قدم إثبات دخل إضافي.", "صلاحية جواز السفر أقل من 6 أشهر؟": "قم بتجديد جواز سفرك."},
        "strateji": "دليل المواعيد المفصل", "detay_metin": "1. تتبع المواعيد: تحقق بين 12:00-02:00 صباحاً. 2. الاستقرار المالي: سجلات آخر 3 أشهر. 3. تنظيم المستندات: حافظ على ترتيب الملفات. 4. الاختصاص القضائي: تحقق من قواعد السفارة. 5. الحجز: تأكد من تأكيد الحجوزات."
    }
}[dil]

# Veri Tabanı
ulke_harc = {"Almanya": 90, "İspanya": 90, "İtalya": 80, "Fransa": 80, "Hollanda": 90}

if 'sayfa' not in st.session_state: st.session_state.sayfa = "Giriş"

# --- EKRANLAR ---
if st.session_state.sayfa == "Giriş":
    st.title(f"✈️ {txt['başlık']}")
    if st.button(txt['başla']):
        st.session_state.sayfa = "Seçim"; st.rerun()

elif st.session_state.sayfa == "Seçim":
    st.title(f"📄 {txt['seçim']}")
    st.session_state.ulke = st.selectbox("Ülke:", list(txt['ülkeler'].keys()))
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(txt['belgeler'])
        st.session_state.secilenler = [e for e in txt['evraklar'] if st.checkbox(e, key=e)]
    with col2:
        st.subheader(txt['risk_başlık'])
        st.session_state.aktif_riskler = [s for s in txt['riskler'].keys() if st.checkbox(s, key=f"chk_{s}")]
        st.session_state.risk_puani = sum([txt['riskler'][s] for s in st.session_state.aktif_riskler])
    if st.button(txt['analiz']):
        st.session_state.sayfa = "Analiz"; st.rerun()

elif st.session_state.sayfa == "Analiz":
    st.title(f"📊 {txt['sonuç']}")
    ihtimal = min(85 + (len(st.session_state.get('secilenler', [])) * 2) - st.session_state.risk_puani, 99)
    st.metric("Onay İhtimali", f"%{max(ihtimal, 5)}")
    if ihtimal < 80:
        st.warning(txt['uyarı'])
        for r in st.session_state.get('aktif_riskler', []): st.error(f"❌ {r} -> **{txt['çözümler'][r]}**")
    if st.button(txt['detay']):
        st.session_state.sayfa = "Detay"; st.rerun()

elif st.session_state.sayfa == "Detay":
    st.title(f"💡 {txt['detay']}")
    st.write(f"Vize Harcı: 90€") # Basitleştirildi
    st.info(txt['strateji'])
    st.markdown(txt['detay_metin'])
    if st.button("Ana Sayfa"):
        st.session_state.sayfa = "Giriş"; st.rerun()