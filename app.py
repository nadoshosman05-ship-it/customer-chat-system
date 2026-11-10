import os
import streamlit as st
from groq import Groq



# تحميل المفتاح من ملف .env


# تهيئة الاتصال بـ OpenAI


# إعداد عنوان الصفحة
st.set_page_config(page_title="نظام خدمة العملاء الذكي", page_icon="🤖")
st.title("🤖 مساعد خدمة العملاء الذكي")
API_KEY = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=API_KEY)
# شخصية النظام
SYSTEM_PROMPT = """
أنت مساعد ذكي جداً لخدمة العملاء في شركة تقنية.
أسلوبك ودود، محترف، ومختصر.
مهمتك الإجابة على استفسارات العملاء حول المنتجات والأسعار وحل المشاكل.
إذا لم تعرف الإجابة، اعتذر بلطف واطلب من العميل التواصل مع الدعم البشري.
"""

# حفظ سجل المحادثة في ذاكرة المتصفح
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# عرض الرسائل السابقة
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# مربع إدخال الرسالة من المستخدم
if prompt := st.chat_input("اكتب رسالتك هنا..."):
    
    # عرض رسالة المستخدم
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})

    # إرسال الطلب للذكاء الاصطناعي وعرض الرد
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=st.session_state.messages,
                temperature=0.7
            )
            full_response = response.choices[0].message.content
            message_placeholder.markdown(full_response)
            
            # إضافة رد الذكاء الاصطناعي للسجل
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            message_placeholder.error(f"حدث خطأ: {str(e)}")