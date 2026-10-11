import streamlit as st
import edge_tts
import asyncio
import os
import time
import re

# စာမျက်နှာ ဖွဲ့စည်းပုံ
st.set_page_config(page_title="StoryLOOP MM - Text to Speech", page_icon="🗣️")

# --- 🌟 မျက်နှာပြင် အလယ် (Main Screen) ---
st.title("Myanmar AI Voice (Unlimited)")
st.write("ဒီ App လေးကို အားလုံး အခမဲ့ အသုံးပြုနိုင်အောင် **StoryLOOP MM** မှ ဖန်တီးပေးထားတာ ဖြစ်ပါတယ်။")

# --- 👀 View Counter ---
st.markdown(
    f"""
    <div style="text-align: center; margin-top: 5px; margin-bottom: 20px;">
        <p style="font-size: 14px; color: gray;">👀 ဝက်ဘ်ဆိုက် ဝင်ရောက်ကြည့်ရှုမှု (Total Views)</p>
        <img src="https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https://storyloopmm.streamlit.app&count_bg=%232EA44F&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=Views&edge_flat=true" alt="View Counter">
    </div>
    """,
    unsafe_allow_html=True
)

youtube_link = "https://youtube.com/@storyloopmm?si=dzQRoGdPAj_2Quno"
st.info(f"ဗီဒီယိုများ ဝင်ရောက်လေ့လာရန် 👉 [**▶️ StoryLOOP MM YouTube Channel သို့ သွားရန် နှိပ်ပါ**]({youtube_link})")
st.write("---")

with st.expander("💡 ပိုမိုကောင်းမွန်သော အသံထွက်ရရှိရန် (ဤနေရာကိုနှိပ်၍ ဖတ်ပါ)", expanded=False):
    st.markdown("""
    - **အသံကို ခဏရပ်စေရန် (Pause):** စာကြောင်းများအဆုံးတွင် **( ။ )** ပုဒ်မ ထည့်ပေးပါ။
    - **အသံအသစ်များ ဖန်တီးနည်း:**
        - 👧🏻 **ကလေးမလေးအသံ:** အမျိုးသမီးအသံ ရွေးပြီး Pitch ကို **+15** မှ **+25** ထားပါ။
        - 👩🏻 **သတင်းကြေညာရှင်:** အမျိုးသမီးအသံ ရွေးပြီး Pitch ကို **-10** ထားပါ။
        - 🧔🏻‍♂️ **လူကြီးသံ:** အမျိုးသားအသံ ရွေးပြီး Pitch ကို **-15** မှ **-25** ထားပါ။
    """)

if "audio_history" not in st.session_state:
    st.session_state.audio_history = []
if "file_counter" not in st.session_state:
    st.session_state.file_counter = 1
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def clear_text():
    st.session_state.input_text = ""

# --- ဇော်ဂျီ အမှားပြင်ဆင်ပေးသည့် Function (Auto-Fix) ---
def fix_myanmar_text(text):
    # ဇော်ဂျီတွင် 'ေ' အား ဗျည်းရှေ့တွင် ရိုက်လေ့ရှိသဖြင့် Unicode ပုံစံ ဗျည်းနောက်သို့ ပြောင်းပေးခြင်း
    fixed_text = re.sub(r'ေ([က-အ])', r'\1ေ', text)
    return fixed_text

st.markdown("### ✏️ စာသားထည့်သွင်းရန်")
st.caption("AI သည် Unicode ကိုသာ အတိအကျ နားလည်ပါသည်။ သင်သည် Zawgyi အသုံးပြုသူဖြစ်ပါက အောက်ပါလင့်ခ်တွင် ယူနီကုဒ်သို့ အရင်ပြောင်းပြီးမှ ထည့်ပေးပါ။")
st.markdown("[👉 ဇော်ဂျီစာသားများကို Unicode သို့ ပြောင်းရန် ဤနေရာကိုနှိပ်ပါ (Rabbit Converter)](https://www.rabbit-converter.org/Rabbit/)")

text_input = st.text_area("ဖတ်ခိုင်းလိုသော စာသားများကို ဤနေရာတွင် ထည့်ပါ...", height=300, key="input_text")

voice_option = st.radio("အဓိက အသံအမျိုးအစား ရွေးချယ်ပါ", ["👩🏻 အမျိုးသမီးအသံ (Nilar)", "👨🏻 အမျိုးသားအသံ (Thiha)"])
voice_code = "my-MM-NilarNeural" if "Nilar" in voice_option else "my-MM-ThihaNeural"

col1, col2 = st.columns(2)
with col1:
    speed = st.slider("အသံ အနှေး/အမြန် (Speed)", -50, 50, -10)
    rate_str = f"{speed:+d}%"
with col2:
    pitch = st.slider("အသံ ကြီး/ငယ် (Pitch)", -50, 50, 0)
    pitch_str = f"{pitch:+d}Hz"

async def create_audio(text, voice, rate, pitch_val, filename):
    processed_text = text.replace('\n', ' ')
    processed_text = processed_text.replace('။', '။\n\n') 
    communicate = edge_tts.Communicate(processed_text, voice, rate=rate, pitch=pitch_val)
    await communicate.save(filename)

btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    generate_clicked = st.button("အသံဖန်တီးပါ (Generate Audio)", type="primary")
with btn_col2:
    st.button("❌ စာသားများကို ဖျက်မည် (Clear)", on_click=clear_text)

if generate_clicked:
    if text_input.strip():
        # စာသားများကို အလိုအလျောက် ပြင်ဆင်ခြင်း
        final_text = fix_myanmar_text(text_input)
        
        current_filename = f"storyloop-{st.session_state.file_counter:07d}.mp3"
        with st.spinner("အသံဖန်တီးနေပါသည်။ ခဏစောင့်ပါ..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_audio(final_text, voice_code, rate_str, pitch_str, current_filename))
                
                st.session_state.audio_history.append(current_filename)
                st.session_state.file_counter += 1
                st.success("အောင်မြင်ပါသည်။ အောက်တွင် နားထောင်နိုင်/ဒေါင်းလုဒ်လုပ်နိုင်ပါသည်။")
            except Exception as e:
                st.error(f"အမှားအယွင်းဖြစ်ပေါ်နေပါသည်: {e}")
    else:
        st.warning("ကျေးဇူးပြု၍ စာသားအရင်ထည့်ပေးပါ။")

if st.session_state.audio_history:
    st.write("---")
    st.subheader("ဖန်တီးထားသော အသံဖိုင်များ")
    for audio_file in reversed(st.session_state.audio_history): 
        if os.path.exists(audio_file):
            st.write(f"🔊 **{audio_file}**")
            st.audio(audio_file, format="audio/mp3")
            with open(audio_file, "rb") as file:
                st.download_button(label=f"⬇️ {audio_file} ကို ဒေါင်းလုဒ်ဆွဲရန်", data=file, file_name=audio_file, mime="audio/mp3", key=audio_file)
