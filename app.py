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

# 🌟 ဒီနေရာမှာ ခေါင်းစဉ်ကို အစ်ကိုလိုချင်တဲ့အတိုင်း ပြောင်းထားပါတယ် 🌟
st.title("Myanmar AI Voice (Unlimited)")

# --- 💡 အသုံးပြုသူများအတွက် အကြံပြုချက်နှင့် လမ်းညွှန် ---
with st.expander("💡 ပိုမိုကောင်းမွန်သော အသံထွက်ရရှိရန် ဖတ်ပါ", expanded=True):
    st.markdown("""
    - **အသံကို ခဏရပ်စေရန် (Pause):** စာများကို တစ်ဆက်တည်း မဖတ်ဘဲ ခဏရပ်စေချင်ပါက စာကြောင်းများအကြားတွင် ပုဒ်ဖြတ်ပုဒ်ရပ်များဖြစ်သော **( ၊ )**၊ **( ။ )** သို့မဟုတ် **( ... )** များကို ထည့်ပေးပါ။ Enter ခေါက်၍ စာပိုဒ်ခွဲရေးခြင်းကလည်း အသံကို သဘာဝကျကျ ရပ်တန့်စေပါသည်။
    - **အကြံပြုထားသော အနှေး/အမြန် နှုန်းထားများ:** 
        - 👩🏻 အမျိုးသမီးအသံ (Nilar) အတွက် **-5%** ကို ထားသုံးရန် အကြံပြုပါသည်။
        - 👨🏻 အမျိုးသားအသံ (Thiha) အတွက် **-10%** ကို ထားသုံးရန် အကြံပြုပါသည်။
    """)
# -----------------------------------------------------------------

# အသံဖိုင်မှတ်တမ်းနှင့် နံပါတ်စဉ်ကို မှတ်သားထားရန်
if "audio_history" not in st.session_state:
    st.session_state.audio_history = []
if "file_counter" not in st.session_state:
    st.session_state.file_counter = 1

# စာသားထည့်ရန်နေရာ
text_input = st.text_area("ဖတ်ခိုင်းလိုသော စာသားများကို ဤနေရာတွင် ထည့်ပါ... (စာအရှည်ကြီး ထည့်လို့ရပါသည်)", height=250)

col1, col2 = st.columns(2)
with col1:
    voice_option = st.radio("အသံရွေးချယ်ပါ", ["အမျိုးသမီးအသံ (Nilar)", "အမျိုးသားအသံ (Thiha)"])
    voice_code = "my-MM-NilarNeural" if voice_option == "အမျိုးသမီးအသံ (Nilar)" else "my-MM-ThihaNeural"

with col2:
    speed = st.slider("အသံ အနှေး/အမြန် ချိန်ညှိရန် (အကြံပြုချက်: မိန်းကလေး -5, ယောကျ်ားလေး -10)", -50, 50, -10)
    rate_str = f"{speed:+d}%"

async def create_audio(text, voice, rate, filename):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(filename)

if st.button("အသံဖန်တီးပါ (Generate Audio)"):
    if text_input.strip():
        current_filename = f"storyloop-{st.session_state.file_counter:07d}.mp3"
        
        with st.spinner(f"{current_filename} ကို ပြောင်းလဲနေပါသည်။ ခဏစောင့်ပါ..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_audio(text_input, voice_code, rate_str, current_filename))
                
                st.session_state.audio_history.append(current_filename)
                st.session_state.file_counter += 1
                
                st.success(f"အောင်မြင်ပါသည်။ {current_filename} ကို အောက်တွင် တွေ့နိုင်ပါသည်။")
            except Exception as e:
                st.error(f"အမှားအယွင်းဖြစ်ပေါ်နေပါသည်: {e}")
    else:
        st.warning("ကျေးဇူးပြု၍ စာသားအရင်ထည့်ပေးပါ။")

# ဖန်တီးထားသော အသံဖိုင်များကို အောက်တွင် စု၍ပြသခြင်း
if st.session_state.audio_history:
    st.write("---")
    st.subheader("ဖန်တီးထားသော အသံဖိုင်များ")
    st.caption("ဤနေရာတွင် ယခင်လုပ်ထားသော အသံများကို ပြန်နားထောင်နိုင်၊ ဒေါင်းလုဒ်ဆွဲနိုင်ပါသည်။")
    
    for audio_file in st.session_state.audio_history:
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
