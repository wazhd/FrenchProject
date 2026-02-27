import asyncio
import os
import edge_tts
import streamlit as st
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
import google.genai as genai
from elevenlabs.client import AsyncElevenLabs
from google.genai import types

load_dotenv()

with open("food-instructions.txt", "r") as file:
    food_instructions = file.read()

with open("art-instructions.txt", "r") as file:
    art_instructions = file.read()

with open("city-instructions.txt", "r") as file:
    city_instructions = file.read()

with open("history-instructions.txt", "r") as file:
    history_instructions = file.read()

with open("music-instructions.txt", "r") as file:
    music_instructions = file.read()

with open("nature-instructions.txt", "r") as file:
    nature_instructions = file.read()

token = os.environ.get("HF_TOKEN")
gemini_api_key_1 = os.environ.get("GEMINI_API_KEY_1")
gemini_api_key_2 = os.environ.get("GEMINI_API_KEY_2")
gemini_api_key_3 = os.environ.get("GEMINI_API_KEY_3")

elevenlabs_api_key_1= os.environ.get("ELEVENLABS_API_KEY_1")
elevenlabs_api_key_2 = os.environ.get("ELEVENLABS_API_KEY_2")

gemini_client_1 = genai.Client(api_key=gemini_api_key_1)
gemini_client_2 = genai.Client(api_key=gemini_api_key_2)
gemini_client_3 = genai.Client(api_key=gemini_api_key_3)


elevenlabs_client_1 = AsyncElevenLabs(api_key=elevenlabs_api_key_1)
elevenlabs_client_2 = AsyncElevenLabs(api_key=elevenlabs_api_key_2)


if "ai_model" not in st.session_state:
    st.session_state.ai_model = "gemini_1"
if "voice_model" not in st.session_state:
    st.session_state.voice_model = "elevenlabs_1"

async def generate_voice(text, voice_id, edge_id, output_path="speech.mp3"):

    if st.session_state.voice_model == "elevenlabs_1":
        try:
            audio = await elevenlabs_client_1.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.8,
                    style=0.0,
                    use_speaker_boost=True,
                    speed=0.5
                )
            )

            with open(output_path, "wb") as f:
                async for chunk in audio:
                    if chunk:
                        f.write(chunk)
            return output_path
        except Exception as e:
            st.session_state.voice_model = "elevenlabs_2"

    if st.session_state.voice_model == "elevenlabs_2":
        try:
            audio = await elevenlabs_client_2.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_multilingual_v2",
                voice_settings=VoiceSettings(
                    stability=0.4,
                    similarity_boost=0.8,
                    style=0.0,
                    use_speaker_boost=True,
                    speed=0.55
                )
            )

            with open(output_path, "wb") as f:
                async for chunk in audio:
                    if chunk:
                        f.write(chunk)
            return output_path
        except Exception as e:
            st.session_state.voice_model = "edge"


    if st.session_state.voice_model == "edge":
        try:

            communicate = edge_tts.Communicate(text, edge_id)
            await communicate.save(output_path)
            return output_path
        except Exception as e:
            st.error("Désolé, un problème est survenu. Veuillez réessayer plus tard.")
            print(str(e))
            return None


async def generate_response(user_input, role):
    if st.session_state.ai_model == "gemini_1":
        try:
            config = types.GenerateContentConfig(
                system_instruction=role, temperature=0.7)
            chat = gemini_client_1.aio.chats.create(model="gemini-3-flash-preview", config=config)
            response = await chat.send_message(user_input)
            return response.text
        except Exception as e:
            st.session_state.ai_model = "gemini_2"
    elif st.session_state.ai_model == "gemini_2":

        try:

            config = types.GenerateContentConfig(

                system_instruction=role, temperature=0.7)

            chat = gemini_client_2.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:
            st.session_state.ai_model = "gemini_3"
    elif st.session_state.ai_model == "gemini_3":

        try:

            config = types.GenerateContentConfig(

                system_instruction=role, temperature=0.7)

            chat = gemini_client_3.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:

            return "Désolé, je ne peux pas répondre pour le moment."


def render_tour_guide(user_question_text, key):
    st.title(voice_map[key]["name"])
    chat_key = f"chat_log_{key}"
    if chat_key not in st.session_state:
        st.session_state[chat_key] = ""

    left, right = st.columns([1, 2])

    with left:
        st.image(f"assets/{key}.jpg")
        user_question = st.text_input(user_question_text)
        ask_button = st.button("Demander", use_container_width=True)

    with right:
        chat_box = st.container(height=500, border=True)
        text_placeholder = chat_box.empty()
        spinner_placeholder = chat_box.empty()

    if ask_button and user_question:
        st.session_state[chat_key] += f"**TOI:** {user_question}\n\n"
        text_placeholder.markdown(st.session_state[chat_key])

        with spinner_placeholder:
            with st.spinner(f"{voice_map[key]['name']} réfléchit..."):
                instructions_map = {
                    "chef": food_instructions,
                    "art": art_instructions,
                    "city": city_instructions,
                    "history": history_instructions,
                    "music": music_instructions,
                    "nature": nature_instructions
                }

                try:
                    loop = asyncio.get_event_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                new_response = loop.run_until_complete(generate_response(user_question, instructions_map[key]))

                st.session_state.current_audio = asyncio.run(generate_voice(
                    new_response,
                    voice_id=voice_map[key]["elevenlabs"],
                    edge_id=voice_map[key]["edge-tts"]
                ))

        spinner_placeholder.empty()
        st.session_state[chat_key] += f"**{voice_map[key]['name'].upper()}:** {new_response}\n\n---\n\n"
        text_placeholder.markdown(st.session_state[chat_key])

    elif st.session_state[chat_key] != "":
        text_placeholder.markdown(st.session_state[chat_key])

    if st.session_state.get("current_audio"):
        st.audio(st.session_state.current_audio, autoplay=True)

    if st.button("Retour"):
        st.session_state.page = "menu"
        st.session_state.current_audio = None
        st.rerun()
voice_map = {
    "chef": {
        "name": "Amélie",
        "edge-tts": "fr-FR-DeniseNeural",
        "elevenlabs": "21m00Tcm4llvDq8ikWAM"
    },
    "city": {
        "name": "Julien",
        "edge-tts": "fr-FR-HenriNeural",
        "elevenlabs": "pNInz6obpguenuvjuc9r"
    },
    "history": {
        "name": "Béatrice",
        "edge-tts": "fr-CA-SylvieNeural",
        "elevenlabs": "MF3mGyEYCl7XYW7Lec9M"
    },
    "nature": {
        "name": "Étienne",
        "edge-tts": "fr-BE-GerardNeural",
        "elevenlabs": "onwK4e9ZLuTAKqzvW80D"
    },
    "music": {
        "name": "Jacques",
        "edge-tts": "fr-FR-RemyMultilingualNeural",
        "elevenlabs": "ErXw7O68Z9Y3v7W9vE2X"
    },
    "art": {
        "name": "Margaux",
        "edge-tts": "fr-CH-ArianeNeural",
        "elevenlabs": "AZnzlk1XhxPjt8VGj9S8"
    }
}