# app.py
import streamlit as st
import requests

st.set_page_config(page_title="Explore Artworks with MET Museum API", page_icon="🎨", layout="centered")

st.title("🎨 Explore Artworks with MET Museum API")
search_term = st.text_input("Search for Artworks:")

if search_term:
    # Step 1: Search for artworks
    search_url = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={search_term}"
    response = requests.get(search_url)
    data = response.json()

    if data["total"] == 0:
        st.warning("No artworks found. Try another keyword.")
    else:
        object_ids = data["objectIDs"][:5]  # show first 5 results
        for obj_id in object_ids:
            obj_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obj_id}"
            obj_data = requests.get(obj_url).json()

            title = obj_data.get("title", "Untitled")
            artist = obj_data.get("artistDisplayName", "Unknown")
            date = obj_data.get("objectDate", "N/A")
            image = obj_data.get("primaryImageSmall", "")
            
            st.subheader(title)
            if image:
                st.image(image, use_container_width=True)
            st.write(f"**Artist:** {artist}")
            st.write(f"**Year:** {date}")
            st.markdown("---")
