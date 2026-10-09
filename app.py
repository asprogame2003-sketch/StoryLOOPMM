import streamlit as st
import edge_tts
import asyncio
import os

st.set_page_config(page_title="My Voice App", page_icon="🗣️")
st.title("မြန်မာ AI အသံထွက် (အကန့်အသတ်မရှိ)")

# အသံဖိုင်မှတ်တမ်းနှင့် နံပါတ်စဉ်ကို မှတ်သားထားရန် (Session State ကို အသုံးပြုခြင်း)
if "audio_history" not in st.session_state:
    st.session_state.audio_history = []
if "file_counter" not in st.session_state:
    st.session_state.file_counter = 1

# စာသားထည့်ရန်နေရာ (max_chars မပါဝင်သဖြင့် အကန့်အသတ်မရှိပါ)
text_input = st.text_area("ဖတ်ခိုင်းလိုသော စာသားများကို ဤနေရာတွင် ထည့်ပါ... (စာအရှည်ကြီး ထည့်လို့ရပါသည်)", height=250)

col1, col2 = st.columns(2)
with col1:
    voice_option = st.radio("အသံရွေးချယ်ပါ", ["အမျိုးသမီးအသံ (Nilar)", "အမျိုးသားအသံ (Thiha)"])
    voice_code = "my-MM-NilarNeural" if voice_option == "အမျိုးသမီးအသံ (Nilar)" else "my-MM-ThihaNeural"

with col2:
    speed = st.slider("အသံ အနှေး/အမြန် ချိန်ညှိရန်", -50, 50, -15)
    rate_str = f"{speed:+d}%"

async def create_audio(text, voice, rate, filename):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(filename)

if st.button("အသံဖန်တီးပါ (Generate Audio)"):
    if text_input.strip():
        # နာမည်ကို storyloop-0000001, 0000002 စသဖြင့် အလိုအလျောက် ပေးခြင်း
        current_filename = f"storyloop-{st.session_state.file_counter:07d}.mp3"
        
        with st.spinner(f"{current_filename} ကို ပြောင်းလဲနေပါသည်။ ခဏစောင့်ပါ..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_audio(text_input, voice_code, rate_str, current_filename))
                
                # ဖန်တီးပြီးသော ဖိုင်နာမည်ကို မှတ်တမ်းထဲသို့ ထည့်ခြင်း
                st.session_state.audio_history.append(current_filename)
                
                # နောက်တစ်ပုဒ်အတွက် နံပါတ်စဉ်တစ်ခု တိုးထားခြင်း
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
    
    # ဖိုင်များကို အစဉ်လိုက် အောက်စီဆင်း၍ ပြပေးမည်
    for audio_file in st.session_state.audio_history:
        if os.path.exists(audio_file):
            st.write(f"🔊 **{audio_file}**")
            st.audio(audio_file, format="audio/mp3")
            
            # ဒေါင်းလုဒ်ဆွဲရန် ခလုတ်
            with open(audio_file, "rb") as file:
                st.download_button(
                    label=f"⬇️ {audio_file} အား ဒေါင်းလုဒ်ဆွဲရန်",
                    data=file,
                    file_name=audio_file,
                    mime="audio/mp3",
                    key=audio_file # ခလုတ်တစ်ခုချင်းစီ မတူစေရန် key ပေးခြင်း
                )
            st.write("") # ခြားထားရန်
