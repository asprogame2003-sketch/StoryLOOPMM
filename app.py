import streamlit as st
import edge_tts
import asyncio
import os
import time

# စာမျက်နှာ ဖွဲ့စည်းပုံ
st.set_page_config(page_title="StoryLOOP MM - Text to Speech", page_icon="🗣️")

# --- 🌟 မျက်နှာပြင် အလယ် (Main Screen) ---
st.title("Myanmar AI Voice (Unlimited)")
st.write("ဒီ App လေးကို အားလုံး အခမဲ့ အသုံးပြုနိုင်အောင် **StoryLOOP MM** မှ ဖန်တီးပေးထားတာ ဖြစ်ပါတယ်။")

# --- ဝက်ဘ်ဆိုက်ကို တစ်ခါဝင်လျှင် (၁) ကြိမ်သာ Count လုပ်ရန် မှတ်သားခြင်း ---
if "visit_id" not in st.session_state:
    st.session_state.visit_id = str(int(time.time()))

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
# -----------------------------------------------------------------

# YouTube Link ကို ခလုတ်ကဲ့သို့ ထင်ရှားအောင် ပြသထားခြင်း
youtube_link = "https://youtube.com/@storyloopmm?si=dzQRoGdPAj_2Quno"
st.info(f"ဗီဒီယိုများ ဝင်ရောက်လေ့လာရန် 👉 [**▶️ StoryLOOP MM YouTube Channel သို့ သွားရန် နှိပ်ပါ**]({youtube_link})")
st.write("---")

# --- 💡 အသုံးပြုသူများအတွက် အကြံပြုချက်နှင့် လမ်းညွှန် (ပိတ်ထားပြီး နှိပ်မှပွင့်မည်) ---
with st.expander("💡 ပိုမိုကောင်းမွန်သော အသံထွက်ရရှိရန် (ဤနေရာကိုနှိပ်၍ ဖတ်ပါ)", expanded=False):
    st.markdown("""
    - **အသံကို ခဏရပ်စေရန် (Pause):** စာကြောင်းများအဆုံးတွင် **( ။ )** ပုဒ်မ ထည့်ပေးပါ။ ( ။ ) တွေ့မှသာ အသံကို သဘာဝကျကျ ခဏရပ်ပေးမည် ဖြစ်ပါသည်။
    - **အသံလုပ်နေစဉ် ရပ်တန့်လိုပါက:** Browser ကို Refresh လုပ်လိုက်ပါ။
    - **အသံအသစ်များ ဖန်တီးနည်း (Pitch ကို အသုံးပြုခြင်း):**
        - 👧🏻 **ကလေးမလေးအသံ/ အသံစူးစူး:** အမျိုးသမီးအသံကို ရွေးပြီး Pitch ကို **+15** မှ **+25** ကြားထားပါ။
        - 👩🏻 **အမျိုးသမီး သတင်းကြေညာရှင်:** အမျိုးသမီးအသံ ရွေးပြီး Pitch ကို **-10** ခန့်ထားပါ။
        - 🧔🏻‍♂️ **လူကြီးသံ/ အသံဩဩ:** အမျိုးသားအသံကို ရွေးပြီး Pitch ကို **-15** မှ **-25** ကြားထားပါ။
    - **အကြံပြုထားသော အနှေး/အမြန် (Speed):** မိန်းကလေး **-5%**, ယောကျ်ားလေး **-10%** (မိမိစိတ်ကြိုက် ထပ်မံချိန်ညှိနိုင်ပါသည်)။
    """)
# -----------------------------------------------------------------

if "audio_history" not in st.session_state:
    st.session_state.audio_history = []
if "file_counter" not in st.session_state:
    st.session_state.file_counter = 1

# --- စာသားများကို Clear ဖျက်ရန် စနစ် ---
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

def clear_text():
    st.session_state.input_text = ""

# စာသားထည့်ရန်နေရာ
text_input = st.text_area("ဖတ်ခိုင်းလိုသော စာသားများကို ဤနေရာတွင် ထည့်ပါ... (စာအရှည်ကြီး ထည့်လို့ရပါသည်)", height=400, key="input_text")

# အသံရွေးချယ်ရန် (Radio Button)
voice_option = st.radio("အဓိက အသံအမျိုးအစား ရွေးချယ်ပါ", ["👩🏻 အမျိုးသမီးအသံ (Nilar)", "👨🏻 အမျိုးသားအသံ (Thiha)"])
voice_code = "my-MM-NilarNeural" if "Nilar" in voice_option else "my-MM-ThihaNeural"

# Speed နှင့် Pitch အတွက် Column ၂ ခုခွဲခြင်း
col1, col2 = st.columns(2)
with col1:
    speed = st.slider("အသံ အနှေး/အမြန် (Speed)", -50, 50, -10)
    rate_str = f"{speed:+d}%"

with col2:
    pitch = st.slider("အသံ ကြီး/ငယ် (Pitch)", -50, 50, 0)
    pitch_str = f"{pitch:+d}Hz"

async def create_audio(text, voice, rate, pitch_val, filename):
    # စာသားကို ပြင်ဆင်ခြင်း: Enter ခေါက်ထားသည်များကို space ဖြင့်အစားထိုးသည်
    processed_text = text.replace('\n', ' ')
    processed_text = processed_text.replace('။', '။ ') 

    communicate = edge_tts.Communicate(processed_text, voice, rate=rate, pitch=pitch_val)
    await communicate.save(filename)

# --- ခလုတ်များကို ယှဉ်လျက်ထားခြင်း ---
btn_col1, btn_col2 = st.columns(2)
with btn_col1:
    generate_clicked = st.button("အသံဖန်တီးပါ (Generate Audio)", type="primary")
with btn_col2:
    st.button("❌ စာသားများကို ဖျက်မည် (Clear)", on_click=clear_text)

if generate_clicked:
    if text_input.strip():
        current_filename = f"storyloop-{st.session_state.file_counter:07d}.mp3"
        
        with st.spinner(f"{current_filename} ကို ပြောင်းလဲနေပါသည်။ ခဏစောင့်ပါ... (ရပ်လိုပါက Refresh လုပ်ပါ)"):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_audio(text_input, voice_code, rate_str, pitch_str, current_filename))
                
                st.session_state.audio_history.append(current_filename)
                st.session_state.file_counter += 1
                
                st.success(f"အောင်မြင်ပါသည်။ {current_filename} ကို အောက်တွင် တွေ့နိုင်ပါသည်။")
            except Exception as e:
                st.error(f"အမှားအယွင်းဖြစ်ပေါ်နေပါသည်: {e}")
    else:
        st.warning("ကျေးဇူးပြု၍ စာသားအရင်ထည့်ပေးပါ။")

if st.session_state.audio_history:
    st.write("---")
    st.subheader("ဖန်တီးထားသော အသံဖိုင်များ")
    st.caption("ဤနေရာတွင် ယခင်လုပ်ထားသော အသံများကို ပြန်နားထောင်နိုင်၊ ဒေါင်းလုဒ်ဆွဲနိုင်ပါသည်။")
    
    for audio_file in reversed(st.session_state.audio_history): 
        if os.path.exists(audio_file):
            st.write(f"🔊 **{audio_file}**")
            st.audio(audio_file, format="audio/mp3")
            
            with open(audio_file, "rb") as file:
                st.download_button(
                    label=f"⬇️ {audio_file} အား ဒေါင်းလုဒ်ဆွဲရန်",
                    data=file,
                    file_name=audio_file,
                    mime="audio/mp3",
                    key=audio_file
                )
            st.write("")
