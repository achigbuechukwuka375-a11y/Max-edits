import streamlit as st
import replicate
import os

st.set_page_config(page_title="Creative AI Studio", page_icon="🎨", layout="wide")
st.title("🎨 Creative AI Multimedia Studio")

# Sidebar for API Keys
st.sidebar.header("🔑 API Configuration")
if "REPLICATE_API_TOKEN" in st.secrets:
    os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]
else:
    replicate_api = st.sidebar.text_input('Enter Replicate API Token', type='password')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Create tabs to organize the app neatly
tab1, tab2, tab3 = st.tabs(["🎭 Face & Video Swap", "🖼️ Photo Editor", "🗣️ Voice Clone"])

# TAB 1: FACE & VIDEO SWAP
with tab1:
    st.header("Face & Video Swapper")
    mode = st.radio("Choose mode:", ["Image Swap", "Video Swap"], key="swap_mode")
    
    if mode == "Image Swap":
        source = st.file_uploader("Upload Source Face", type=['jpg', 'png'], key="img_src")
        target = st.file_uploader("Upload Target Image", type=['jpg', 'png'], key="img_tgt")
        model_id = "codeplugtech/face-swap:278a81e7ebb22db98bcba54de985d22cc1abeead2754eb1f2af717247be69b34"
        input_params = {"input_image": source, "swap_image": target}
    else:
        source = st.file_uploader("Upload Source Face (Image)", type=['jpg', 'png'], key="vid_src")
        target = st.file_uploader("Upload Target Video (MP4)", type=['mp4', 'mov'], key="vid_tgt")
        model_id = "xrunda/hello:104b4a39315349db50880757bc8c1c996c5309e3aa11286b0a3c84dab81fd440"
        input_params = {"target": target, "source": source}

    if st.button("🚀 Start Swapping"):
        if not os.environ.get('REPLICATE_API_TOKEN'):
            st.error("Please provide a Replicate API token.")
        elif source and target:
            with st.spinner("AI is working..."):
                try:
                    output = replicate.run(model_id, input=input_params)
                    st.success("Complete!")
                    st.image(output) if mode == "Image Swap" else st.video(output)
                except Exception as e:
                    st.error(f"Error: {e}")

# TAB 2: PHOTO EDITOR
with tab2:
    st.header("AI Photo Editor & Enhancer")
    editor_input = st.file_uploader("Upload Image to Edit", type=['jpg', 'png', 'jpeg'], key="edit_input")
    if st.button("✨ Upscale Image"):
        if not os.environ.get('REPLICATE_API_TOKEN'):
            st.error("Please add your Replicate API key.")
        elif editor_input:
            with st.spinner("Enhancing..."):
                try:
                    output = replicate.run(
                        "tencentarc/gfpgan:0fbacf7af1601de355b9961cd97aa46150d4a9bfbe701dee88c347343f54a65d",
                        input={"img": editor_input}
                    )
                    st.image(output, caption="Enhanced Result")
                except Exception as e:
                    st.error(f"Error: {e}")

# TAB 3: VOICE CLONE
with tab3:
    st.header("AI Voice Cloning")
    voice_sample = st.file_uploader("Upload Voice Sample (WAV/MP3)", type=['wav', 'mp3'])
    text_to_speak = st.text_area("What should the voice say?", "Hello!")
    if st.button("🗣️ Generate Voice"):
        if not os.environ.get('REPLICATE_API_TOKEN'):
            st.error("Please add your Replicate API key.")
        elif voice_sample and text_to_speak:
            with st.spinner("Cloning voice..."):
                try:
                    output = replicate.run(
                        "lucataco/xtts-v2:6841e085bda86659a7a723af89db62af7db2256598da698c0919dbfb80946059",
                        input={"speaker_audio": voice_sample, "text": text_to_speak, "language": "en"}
                    )
                    st.audio(output)
                except Exception as e:
                    st.error(f"Error: {e}")
