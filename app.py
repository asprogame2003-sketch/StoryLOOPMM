import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="My Voice App", page_icon="🗣️")
st.title("မြန်မာ AI အသံထွက် (အကန့်အသတ်မရှိ)")

# ဒီနေရာမှာ max_chars မထည့်ထားတဲ့အတွက် စာလုံးရေ အကန့်အသတ်မရှိ (စာအုပ်တစ်အုပ်စာအထိ) ထည့်လို့ရပါပြီ
text_input = st.text_area("ဖတ်ခိုင်းလိုသော စာသားများကို ဤနေရာတွင် ထည့်ပါ... (စာအရှည်ကြီး ထည့်လို့ရပါသည်)", height=350)

col1, col2 = st.columns(2)
with col1:
    voice_option = st.radio("အသံရွေးချယ်ပါ", ["အမျိုးသမီးအသံ (Nilar)", "အမျိုးသားအသံ (Thiha)"])
    voice_code = "my-MM-NilarNeural" if voice_option == "အမျိုးသမီးအသံ (Nilar)" else "my-MM-ThihaNeural"

with col2:
    # အသံ အနှေးအမြန် ချိန်ညှိရန် (အနှုတ်ပြလျှင် နှေးမည်၊ အပေါင်းပြလျှင် မြန်မည်)
    # -15% သည် လူပြောသည့်အသံနှုန်းနှင့် အနီးစပ်ဆုံးဖြစ်သည်
    speed = st.slider("အသံ အနှေး/အမြန် ချိန်ညှိရန်", -50, 50, -15)
    rate_str = f"{speed:+d}%"

async def create_audio(text, voice, rate):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save("output.mp3")

if st.button("အသံဖန်တီးပါ (Generate Audio)"):
    if text_input.strip():
        with st.spinner("အသံအဖြစ်သို့ ပြောင်းလဲနေပါသည်။ စာရှည်ပါက အနည်းငယ် ပိုစောင့်ပေးပါ..."):
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                loop.run_until_complete(create_audio(text_input, voice_code, rate_str))
                
                st.audio("output.mp3", format="audio/mp3")
                st.success("အောင်မြင်စွာ ပြောင်းလဲပြီးပါပြီ!")
            except Exception as e:
                st.error(f"အမှားအယွင်းဖြစ်ပေါ်နေပါသည်: {e}")
    else:
        st.warning("ကျေးဇူးပြု၍ စာသားအရင်ထည့်ပေးပါ။")
