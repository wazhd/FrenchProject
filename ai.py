import asyncio
import os
import edge_tts
import streamlit as st
from dotenv import load_dotenv
from elevenlabs import VoiceSettings
import google.genai as genai
from elevenlabs.client import AsyncElevenLabs
from google.genai import types
from gradio_client import Client

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

llama_client = True
gemma_client = True

token_1 = os.environ.get("HF_TOKEN")
token_2 = os.environ.get("HF_TOKEN_2")
try:
    llama_client_1 = Client("huggingface-projects/llama-3.2-3B-Instruct", token=token_1)
    llama_client_2 = Client("huggingface-projects/llama-3.2-3B-Instruct", token=token_2)
except Exception as e:
    llama_client = False

try:
    gemma_client_1 = Client("huggingface-projects/gemma-3-12b-it", token=token_1)
    gemma_client_2 = Client("huggingface-projects/gemma-3-12b-it", token=token_2)

except Exception as e:
    gemma_client = False



gemini_api_key_1 = os.environ.get("GEMINI_API_KEY_1")
gemini_api_key_2 = os.environ.get("GEMINI_API_KEY_2")
gemini_api_key_3 = os.environ.get("GEMINI_API_KEY_3")
gemini_api_key_4 = os.environ.get("GEMINI_API_KEY_4")

elevenlabs_api_key_1= os.environ.get("ELEVENLABS_API_KEY_1")
elevenlabs_api_key_2 = os.environ.get("ELEVENLABS_API_KEY_2")

gemini_client_1 = genai.Client(api_key=gemini_api_key_1)
gemini_client_2 = genai.Client(api_key=gemini_api_key_2)
gemini_client_3 = genai.Client(api_key=gemini_api_key_3)
gemini_client_4 = genai.Client(api_key=gemini_api_key_4)


elevenlabs_client_1 = AsyncElevenLabs(api_key=elevenlabs_api_key_1)
elevenlabs_client_2 = AsyncElevenLabs(api_key=elevenlabs_api_key_2)


async def generate_voice(text, voice_id, edge_id, output_path="speech.mp3"):
    if st.session_state.voice_model == "elevenlabs_1":
        try:
            response = elevenlabs_client_1.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_v3",
                voice_settings=VoiceSettings(stability=0.4, similarity_boost=0.8, speed=0.7),
                output_format="mp3_44100_128",
            )

            with open(output_path, "wb") as f:
                async for chunk in response:
                    if chunk:
                        f.write(chunk)

            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
        except Exception as e:
            st.session_state.voice_model = "elevenlabs_2"

    if st.session_state.voice_model == "elevenlabs_2":
        try:
            response = elevenlabs_client_2.text_to_speech.convert(
                text=text,
                voice_id=voice_id,
                model_id="eleven_v3",
                voice_settings=VoiceSettings(stability=0.4, similarity_boost=0.8, speed=0.7),
                output_format="mp3_44100_128",
            )
            with open(output_path, "wb") as f:
                async for chunk in response:
                    if chunk:
                        f.write(chunk)

            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return output_path
        except Exception as e:
            st.session_state.voice_model = "edge"


    if st.session_state.voice_model == "edge":
        try:
            communicate = edge_tts.Communicate(text, edge_id)
            await communicate.save(output_path)
            return output_path
        except Exception as e:
            st.error("Audio generation failed completely.")
            return None

async def generate_response(user_input, role, history):
    if st.session_state.ai_model == "gemini_1":
        try:
            config = types.GenerateContentConfig(
                system_instruction=role + "|| Chat History: " + history, temperature=0.7)
            chat = gemini_client_1.aio.chats.create(model="gemini-3-flash-preview", config=config)
            response = await chat.send_message(user_input)
            return response.text
        except Exception as e:
            st.session_state.ai_model = "gemini_2"
    if st.session_state.ai_model == "gemini_2":

        try:

            config = types.GenerateContentConfig(

                system_instruction=f"REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: {role} + \n\n Chat History: {history}. \n\n Respond only in French.", temperature=0.7)

            chat = gemini_client_2.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:
            st.session_state.ai_model = "gemini_3"
    if st.session_state.ai_model == "gemini_3":

        try:

            config = types.GenerateContentConfig(

                system_instruction=f"REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: {role} + \n\n Chat History: {history}. \n\n Respond only in French.", temperature=0.7)

            chat = gemini_client_3.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:

            st.session_state.ai_model = "gemini_4"
    if st.session_state.ai_model == "gemini_4":
        try:

            config = types.GenerateContentConfig(

                system_instruction=f"REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: {role} + \n\n Chat History: {history}. \n\n Respond only in French.", temperature=0.7)

            chat = gemini_client_4.aio.chats.create(model="gemini-3-flash-preview", config=config)

            response = await chat.send_message(user_input)

            return response.text

        except Exception as e:
            st.session_state.ai_model = "llama_1"

    if llama_client:
        if st.session_state.ai_model == "llama_1":
            try:
                result = await asyncio.to_thread(
                    llama_client_1.predict,
                    message=f"REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: {role} + \n\n Chat History: {history}. \n\n Respond only in French. User says: {user_input}",
                    max_new_tokens=1024,
                    temperature=0.7,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.2,
                    api_name="/generate"
                )
                return result
            except Exception as e:
                st.session_state.ai_model = "llama_2"


        if st.session_state.ai_model == "llama_2":
            try:
                result = await asyncio.to_thread(
                    llama_client_2.predict,
                    message=f"REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: {role} + \n\n Chat History: {history}. \n\n Respond only in French. User says: {user_input}",
                    max_new_tokens=1024,
                    temperature=0.7,
                    top_p=0.9,
                    top_k=50,
                    repetition_penalty=1.2,
                    api_name="/generate"
                )
                return result
            except Exception as e:
                st.session_state.ai_model = "gemma_1"
    if gemma_client:
        if st.session_state.ai_model == "gemma_1":
            try:
                result = await asyncio.to_thread(
                    gemma_client_1.predict,
                    message={"text": user_input, "files": []},
                    system_prompt=f"REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: {role} + \n\n Chat History: {history}. \n\n Respond only in French.",
                    max_new_tokens=700,
                    api_name="/run"
                )

                return result
            except Exception as e:
                st.session_state.ai_model = "gemma_2"

        if st.session_state.ai_model == "gemma_2":
            try:
                result = await asyncio.to_thread(
                    gemma_client_2.predict,
                    message={"text": user_input, "files": []},
                    system_prompt=f"REMEMBER THESE INSTRUCTIONS VERY CAREFULLY: {role} + \n\n Chat History: {history}. \n\n Respond only in French.",
                    max_new_tokens=700,
                    api_name="/run"
                )
                return result
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

                async def process_chat():
                    text = await generate_response(user_question, instructions_map[key], st.session_state[chat_key])
                    if not text:
                        text = "Désolé, je ne peux pas répondre pour le moment."

                    audio = await generate_voice(text, voice_map[key]["elevenlabs"], voice_map[key]["edge-tts"])
                    return text, audio

                new_response, st.session_state.current_audio = asyncio.run(process_chat())

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


def quiz():
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False

    st.title("🧩 Quiz interactif : Toronto et sa culture")
    st.write("Testez vos connaissances sur la francophonie et la culture torontoise après notre présentation !")


    with st.form("quiz_form"):
        q1 = st.radio(
            "1. En quelle année Samuel de Champlain est-il arrivé pour explorer la région ?",
            ["1534", "1615", "1790", "1803"],
            index=None
    )

    q2 = st.radio(
        "2. Quel pourcentage de la population de Toronto avait le français comme langue maternelle en 2021 ?",
        ["1,5 %", "3,7 %", "10 %", "12,4 %"],
        index=None

    )

    q3 = st.radio(
        "3. Quel est l'ingrédient principal qui compose la base de la 'Sushi Pizza' à Toronto ?",
        ["Pâte à pizza classique", "Pain pita", "Riz frit", "Feuille d'algue séchée"],
        index=None

    )

    q4 = st.radio(
        "4. Quel quartier est connu pour être le premier projet de logement social au Canada ?",
        ["Corktown", "Little Italy", "Old Town", "Regent Park"],
        index=None

    )

    q5 = st.radio(
        "5. Pendant combien de temps la Tour CN a-t-elle été la plus haute tour du monde ?",
        ["10 ans", "20 ans", "Plus de 30 ans", "Elle l'est toujours"],
        index=None

    )

    submit_button = st.form_submit_button("Soumettre mes réponses")


    if submit_button:
        st.session_state.score = 0
        st.session_state.submitted = True
    
        if q1 == "1615": st.session_state.score += 1
        if q2 == "3,7 %": st.session_state.score += 1
        if q3 == "Riz frit": st.session_state.score += 1
        if q4 == "Regent Park": st.session_state.score += 1
        if q5 == "Plus de 30 ans": st.session_state.score += 1
    
        st.divider()
        if st.session_state.score == 5:
            st.balloons()
            st.success(f"Félicitations ! Score parfait : {st.session_state.score}/5 🏆")
        elif st.session_state.score >= 3:
            st.info(f"Pas mal ! Ton score est de : {st.session_state.score}/5 👍")
        else:
            st.warning(f"Tu peux faire mieux ! Score : {st.session_state.score}/5. Relis le script !")


voice_map = {
    "chef": {
        "name": "Amélie",
        "edge-tts": "fr-FR-DeniseNeural",
        "elevenlabs": "hpp4J3VqNfWAUOO0d1Us"
    },
    "city": {
        "name": "Julien",
        "edge-tts": "fr-FR-HenriNeural",
        "elevenlabs": "iP95p4xoKVk53GoZ742B"
    },
    "history": {
        "name": "Béatrice",
        "edge-tts": "fr-CA-SylvieNeural",
        "elevenlabs": "EXAVITQu4vr4xnSDxMaL"
    },
    "nature": {
        "name": "Étienne",
        "edge-tts": "fr-BE-GerardNeural",
        "elevenlabs": "SAz9YHcvj6GT2YYXdXww"
    },
    "music": {
        "name": "Jacques",
        "edge-tts": "fr-FR-RemyMultilingualNeural",
        "elevenlabs": "CwhRBWXzGAHq8TQ4Fs17"
    },
    "art": {
        "name": "Margaux",
        "edge-tts": "fr-CH-ArianeNeural",
        "elevenlabs": "Xb7hH8MSUJpSbSDYk0k2"
    }
}
