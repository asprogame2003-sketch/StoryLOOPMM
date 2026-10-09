import streamlit as st
import edge_tts
import asyncio
import os

# စာမျက်နှာ ဖွဲ့စည်းပုံ
st.set_page_config(page_title="StoryLOOP MM - Text to Speech", page_icon="🗣️")

# --- ဘေးဘက် (Sidebar) တွင် YouTube Channel အကြောင်းထည့်ရန် ---
st.sidebar.title("✨ ဖန်တီးသူအကြောင်း")
st.sidebar.write("ဒီ App လေးကို အားလုံး အခမဲ့ အသုံးပြုနိုင်အောင် ဖန်တီးပေးထားတာ ဖြစ်ပါတယ်။")
st.sidebar.write("ကျွန်တော့်ရဲ့ YouTube Channel မှာလည်း ဗီဒီယိုတွေ ဝင်ရောက်လေ့လာပြီး အားပေးနိုင်ပါတယ်ခင်ဗျာ။ 👇")

youtube_link = "https://youtube.com/@storyloopmm?si=dzQRoGdPAj_2Quno" 
st.sidebar.markdown(f"[**▶️ YouTube Channel သို့ သွားရန် နှိပ်ပါ**]({youtube_link})")
st.sidebar.write("---")
st.sidebar.caption("Created by: StoryLOOP MM")
# -----------------------------------------------------------

st.title("Myanmar AI Voice (Unlimited)")

# --- 💡 အသုံးပြုသူများအတွက် အကြံပြုချက်နှင့် လမ်းညွှန် ---
with st.expander("💡 အသံအသစ်များ ဖန်တီးနည်းနှင့် အကြံပြုချက်များ (ဖတ်ရန်)", expanded=True):
    st.markdown("""
    - **အသံကို ခဏရပ်စေရန် (Pause):** စာကြောင်းများအကြားတွင် ပုဒ်ဖြတ်ပုဒ်ရပ်များ **( ၊ )**၊ **( ။ )** သို့မဟုတ် **( ... )** ထည့်ပေးပါ။ (သို့) Enter ခေါက်၍ စာပိုဒ်ခွဲရေးပါ။
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

text_input = st.text_area("ဖတ်ခိုင်းလိုသော စာသားများကို ဤနေရာတွင် ထည့်ပါ... (စာအရှည်ကြီး ထည့်လို့ရပါသည်)", height=200)

# အသံရွေးချယ်ရန် (Radio Button)
voice_option = st.radio("အဓိက အသံအမျိုးအစား ရွေးချယ်ပါ", ["👩🏻 အမျိုးသမီးအသံ (Nilar)", "👨🏻 အမျိုးသားအသံ (Thiha)"])
voice_code = "my-MM-NilarNeural" if "Nilar" in voice_option else "my-MM-ThihaNeural"

# Speed နှင့် Pitch အတွက် Column ၂ ခုခွဲခြင်း
col1, col2 = st.columns(2)
with col1:
    speed = st.slider("အသံ အနှေး/အမြန် (Speed)", -50, 50, -10)
    rate_str = f"{speed:+d}%"

with col2:
    # 🌟 အသံအသစ်များ ဖန်တီးရန် Pitch Slider အသစ် 🌟
    pitch = st.slider("အသံ ကြီး/ငယ် (Pitch)", -50, 50, 0)
    pitch_str = f"{pitch:+d}Hz"

async def create_audio(text, voice, rate, pitch_val, filename):
    # Pitch ပါ ထည့်သွင်း အလုပ်လုပ်စေရန် ပြင်ဆင်ထားသည်
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch_val)
    await communicate.save(filename)

if st.button("အသံဖန်တီးပါ (Generate Audio)"):
    if text_input.strip():
        current_filename = f"storyloop-{st.session_state.file_counter:07d}.mp3"
        
        with st.spinner(f"{current_filename} ကို ပြောင်းလဲနေပါသည်။ ခဏစောင့်ပါ..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                # create_audio ထဲသို့ pitch_str ကိုပါ ထည့်သွင်းပေးပို့သည်
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
    
    for audio_file in reversed(st.session_state.audio_history): # အသစ်လုပ်ထားသောဖိုင်ကို အပေါ်ဆုံးတွင်ပြရန် reversed သုံးထားပါသည်
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
