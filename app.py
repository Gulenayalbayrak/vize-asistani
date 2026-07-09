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
        "belgeler": "Gerekli Belgeler (*: Zorunlu)", "risk_başlık": "⚠️ Risk Soruları",
        "ülkeler": ["Almanya", "İspanya", "İtalya", "Fransa", "Hollanda", "Yunanistan", "Avusturya", "Belçika", "İsveç", "İsviçre"],
        "evraklar": ["Pasaport*", "Sigorta Poliçesi*", "Uçak Rezervasyonu*", "Otel Rezervasyonu", "Banka Hesap Dökümü", "Maaş Bordrosu", "Tapu", "Araç", "Davetiye"],
        "riskler": {"Daha önce vize reddi aldınız mı?": 20, "Düzenli geliriniz yok mu?": 25, "Pasaport süresi 6 aydan az mı?": 30},
        "uyarı": "Vize alma olasılığınız aşağıdaki sebeplerden dolayı düşüktür:",
        "çözümler": {"Daha önce vize reddi aldınız mı?": "Red gerekçesini açıklayan bir ön yazı hazırlayın.", "Düzenli geliriniz yok mu?": "Ek gelir veya sponsor belgesi ekleyin.", "Pasaport süresi 6 aydan az mı?": "Pasaportunuzu yenileyin."},
        "strateji": "Randevu ve Başvuru Rehberi",
        "detay_liste": "- Vize Ücreti: 90€ (Hizmet bedeli hariçtir).\n- Randevu takibi: Gece 00-02 arası sistemleri kontrol edin.\n- Finansal istikrar: Son 3 aylık hesap hareketleri düzenli olmalı.\n- Evrak düzeni: Asıllar ve fotokopiler ayrı dosyalarda olmalı.\n- İkametgah: Yetkili aracı kurumun doğru seçildiğinden emin olun.",
        "başarı": "Vize alma olasılığınız oldukça yüksek, başvurunuz kolaylıkla onaylanabilir.",
        "tavsiye": "Başvurunuzu daha da güçlendirmek için şu belgeleri eklemeyi değerlendirebilirsiniz:"
    },
    "English": {
        "başlık": "Visa Expert Portal", "başla": "Start Application", "seçim": "Documents & Risk", 
        "analiz": "Go to Analysis", "sonuç": "Analysis Result", "detay": "Details & Appointment",
        "belgeler": "Required Documents (*: Mandatory)", "risk_başlık": "⚠️ Risk Factors",
        "ülkeler": ["Germany", "Spain", "Italy", "France", "Netherlands", "Greece", "Austria", "Belgium", "Sweden", "Switzerland"],
        "evraklar": ["Passport*", "Insurance Policy*", "Flight Reservation*", "Hotel Reservation", "Bank Statement", "Salary Slip", "Deed", "Vehicle", "Invitation"],
        "riskler": {"Have you been refused a visa before?": 20, "No regular income?": 25, "Passport valid less than 6 months?": 30},
        "uyarı": "Your visa probability is low due to the following:",
        "çözümler": {"Have you been refused a visa before?": "Prepare a cover letter.", "No regular income?": "Provide proof of additional income.", "Passport valid less than 6 months?": "Renew your passport."},
        "strateji": "Appointment and Application Guide",
        "detay_liste": "- Visa Fee: 90€ (Service fee excluded).\n- Appointment tracking: Check systems between 00:00-02:00 AM.\n- Financial stability: Consistent records for the last 3 months.\n- Document order: Originals and copies should be separated.\n- Jurisdiction: Verify embassy rules for your residence.",
        "başarı": "Your visa probability is quite high, your application can be easily approved.",
        "tavsiye": "To strengthen your application, consider adding these documents:"
    },
    "العربية": {
        "başlık": "بوابة خبير التأشيرات", "başla": "ابدأ الطلب", "seçim": "المستندات والمخاطر", 
        "analiz": "اذهب إلى التحليل", "sonuç": "نتيجة التحليل", "detay": "التفاصيل والموعد",
        "belgeler": "المستندات المطلوبة (*: إلزامي)", "risk_başlık": "⚠️ عوامل الخطر",
        "ülkeler": ["ألمانيا", "إسبانيا", "إيطاليا", "فرنسا", "هولندا", "اليونان", "النمسا", "بلجيكا", "السويد", "سويسرا"],
        "evraklar": ["جواز السفر*", "بوليصة التأمين*", "حجز الطيران*", "حجز الفندق", "كشف حساب بنكي", "قسيمة الراتب", "سند الملكية", "مركبة", "دعوة"],
        "riskler": {"هل سبق لك رفض التأشيرة؟": 20, "لا يوجد دخل منتظم؟": 25, "صلاحية جواز السفر أقل من 6 أشهر؟": 30},
        "uyarı": "احتمالية الحصول على التأشيرة منخفضة للأسباب التالية:",
        "çözümler": {"هل سبق لك رفض التأشيرة؟": "قم بإعداد خطاب توضيحي.", "لا يوجد دخل منتظم؟": "قدم إثبات دخل إضافي.", "صلاحية جواز السفر أقل من 6 أشهر؟": "قم بتجديد جواز سفرك."},
        "strateji": "دليل المواعيد والتقديم",
        "detay_liste": "- رسوم التأشيرة: 90 يورو (بدون رسوم الخدمة).\n- تتبع المواعيد: تحقق بين 12:00-02:00 صباحاً.\n- الاستقرار المالي: سجلات آخر 3 أشهر.\n- ترتيب المستندات: حافظ على ترتيب الملفات.\n- الاختصاص القضائي: تحقق من قواعد السفارة.",
        "başarı": "فرصتك في الحصول على التأشيرة عالية جداً، ويمكن الموافقة على طلبك بسهولة.",
        "tavsiye": "لتعزيز طلبك، فكر في إضافة هذه المستندات:"
    }
}[dil]

if 'sayfa' not in st.session_state: st.session_state.sayfa = "Giriş"

# --- EKRANLAR ---
if st.session_state.sayfa == "Giriş":
    st.title(f"✈️ {txt['başlık']}")
    if st.button(txt['başla']):
        st.session_state.sayfa = "Seçim"; st.rerun()

elif st.session_state.sayfa == "Seçim":
    st.title(f"📄 {txt['seçim']}")
    st.session_state.ulke = st.selectbox("Ülke / Country / البلد:", txt['ülkeler'])
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