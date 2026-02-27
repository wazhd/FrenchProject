import streamlit as st
import ai

st.set_page_config(page_title="Guides de Toronto", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "menu"

if "ai_model" not in st.session_state:
    st.session_state.ai_model = "gemini"

if "voice_model" not in st.session_state:
    st.session_state.voice_model = "edge"

if st.session_state.page == "menu":
    st.title("Découvrez Toronto : Cliquez sur un guide pour en apprendre plus")

    with st.container(border=True):
        left, right = st.columns([1.2, 1])
        with left:
            st.image("assets/music.jpg")
        with right:
            st.markdown("# Jacques")
            st.markdown("### Expert en Musique de Toronto")
            if st.button("Parler avec Jacques", key="btn_jacques", use_container_width=True):
                st.session_state.page = "music"
                st.rerun()

    with st.container(border=True):
        left, right = st.columns([0.6, 1])
        with left:
            st.image("assets/nature.jpg", use_container_width=True)
        with right:
            st.markdown("# Étienne")
            st.markdown("### Expert en Nature et Parcs de Toronto")
            if st.button("Parler avec Étienne", key="btn_etienne", use_container_width=True):
                st.session_state.page = "nature"
                st.rerun()

    with st.container(border=True):
        left, right = st.columns([1.2, 1])
        with left:
            st.image("assets/history.jpg")
        with right:
            st.markdown("# Béatrice")
            st.markdown("### Experte en Histoire de Toronto")
            if st.button("Parler avec Béatrice", key="btn_beatrice", use_container_width=True):
                st.session_state.page = "history"
                st.rerun()

    with st.container(border=True):
        left, right = st.columns([1.2, 1])
        with left:
            st.image("assets/chef.jpg")
        with right:
            st.markdown("# Amélie")
            st.markdown("### Experte en scène culinaire et restaurants à Toronto")
            if st.button("Parler avec Amélie", key="btn_amelie", use_container_width=True):
                st.session_state.page = "chef"
                st.rerun()

    with st.container(border=True):
        left, right = st.columns([1.2, 1])
        with left:
            st.image("assets/art.jpg")
        with right:
            st.markdown("# Margaux")
            st.markdown("### Experte en Arts et Culture de Toronto")
            if st.button("Parler avec Margaux", key="btn_margaux", use_container_width=True):
                st.session_state.page = "art"
                st.rerun()

    with st.container(border=True):
        left, right = st.columns([1.2, 1])
        with left:
            st.image("assets/city.jpg")
        with right:
            st.markdown("# Julien")
            st.markdown("### Expert en transports, monuments et sorties à Toronto")
            if st.button("Parler avec Julien", key="btn_julien", use_container_width=True):
                st.session_state.page = "city"
                st.rerun()

elif st.session_state.page == "music":
    ai.render_tour_guide("Posez votre question à Jacques sur la musique à Toronto...", "music")

elif st.session_state.page == "nature":
    ai.render_tour_guide("Posez votre question à Étienne sur la nature à Toronto...", "nature")

elif st.session_state.page == "history":
    ai.render_tour_guide("Posez votre question à Béatrice sur l'histoire à Toronto...", "history")

elif st.session_state.page == "chef":
    ai.render_tour_guide("Posez votre question à Amélie sur les restaurants à Toronto...", "chef")

elif st.session_state.page == "art":
    ai.render_tour_guide("Posez votre question à Margaux sur l'art à Toronto...", "art")

elif st.session_state.page == "city":
    ai.render_tour_guide("Posez votre question à Julien sur les monuments et activités à Toronto...", "city")