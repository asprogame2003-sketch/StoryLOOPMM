import streamlit as st
import edge_tts
import asyncio
import os
import tempfile
import shutil

try:
    from pydub import AudioSegment
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False

st.set_page_config(page_title="StoryLoop MM Voice", page_icon="🎙️")
st.title("🎙️ StoryLoop MM - AI Voice App")
st.write("အသံပြောင်းလိုသော စာသားများကို အောက်တွင် ရေးပါ သို့မဟုတ် Paste လုပ်ပါ။")

text_input = st.text_area("စာသားထည့်ရန် အကွက်", height=200)

voice_choice = st.selectbox(
    "အသံရွေးချယ်ပါ",
    options=["my-MM-ThihaNeural", "my-MM-NilarNeural"],
    format_func=lambda x: "👨 ယောကျ်ားလေးအသံ (Thiha)" if x == "my-MM-ThihaNeural" else "👩 မိန်းကလေးအသံ (Nilar)"
)

if st.button("အသံဖိုင် ဖန်တီးပါ", type="primary"):
    if not text_input.strip():
        st.warning("ကျေးဇူးပြု၍ စာသားတစ်ခုခု ရေးထည့်ပါ။")
    else:
        with st.spinner("⏳ အသံဖန်တီးနေပါသည်... ခဏစောင့်ပါ။ (စာသားရှည်ပါက အချိန်အနည်းငယ် ကြာနိုင်ပါသည်)"):
            async def generate_audio():
                paragraphs = [p.strip() for p in text_input.split('\n') if p.strip()]
                temp_dir = tempfile.mkdtemp()
                temp_files = []
                final_path = os.path.join(temp_dir, "AI_Voice.mp3")
                
                try:
                    # စာပိုဒ်တစ်ခုချင်းစီကို အသံဖန်တီးခြင်း
                    for i, para in enumerate(paragraphs):
                        t_file = os.path.join(temp_dir, f"temp_{i}.mp3")
                        communicate = edge_tts.Communicate(para, voice_choice)
                        await communicate.save(t_file)
                        temp_files.append(t_file)
                    
                    # အသံဖိုင်များ ပေါင်းခြင်း
                    if PYDUB_AVAILABLE and len(temp_files) > 1:
                        final_audio = AudioSegment.empty()
                        silence = AudioSegment.silent(duration=2000) # ၂ စက္ကန့်စီခြားမည်
                        for idx, t_file in enumerate(temp_files):
                            final_audio += AudioSegment.from_mp3(t_file)
                            if idx < len(temp_files) - 1:
                                final_audio += silence
                        final_audio.export(final_path, format="mp3")
                    else:
                        shutil.copy(temp_files[0], final_path)
                    
                    return final_path
                except Exception as e:
                    st.error(f"အမှားအယွင်းဖြစ်နေပါသည်: {e}")
                    return None
            
            output_file = asyncio.run(generate_audio())
            
            if output_file and os.path.exists(output_file):
                st.success("✅ အောင်မြင်စွာ ဖန်တီးပြီးပါပြီ။")
                with open(output_file, "rb") as f:
                    st.download_button(
                        label="📥 အသံဖိုင် (MP3) ဒေါင်းလုဒ်လုပ်ရန်",
                        data=f,
                        file_name="AI_Voice.mp3",
                        mime="audio/mp3"
                    )