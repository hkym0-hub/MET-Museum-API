import streamlit as st
import requests
import random

# --- MET API base URLs ---
SEARCH_URL = "https://collectionapi.metmuseum.org/public/collection/v1/search"
OBJECT_URL = "https://collectionapi.metmuseum.org/public/collection/v1/objects"

st.title("🖼️ MET Museum Art Explorer")

# --- Function 1: Search artworks by keyword ---
def search_artworks(query, department_id=None):
    params = {"q": query}
    if department_id:
        params["departmentId"] = department_id
    response = requests.get(SEARCH_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("objectIDs", [])
    else:
        return []

# --- Function 2: Get artwork details ---
def get_artwork_details(object_id):
    response = requests.get(f"{OBJECT_URL}/{object_id}")
    if response.status_code == 200:
        return response.json()
    else:
        return None

# --- Function 3: Random artwork (이미지 있는 작품만) ---
def random_artwork():
    # hasImages=True 옵션으로 검색
    response = requests.get(SEARCH_URL, params={"q":"*", "hasImages":True})
    if response.status_code == 200:
        data = response.json()
        object_ids = data.get("objectIDs", [])
        if object_ids:
            # 이미지 있는 작품 중 랜덤 선택
            random_id = random.choice(object_ids)
            return get_artwork_details(random_id)
    return None

# --- Department selection ---
departments = {
    "None": None,
    "American Decorative Arts": 1,
    "Ancient Near Eastern Art": 3,
    "Arms and Armor": 4,
    "Arts of Africa, Oceania, and the Americas": 5,
    "Asian Art": 6,
    "Costume Institute": 7,
    "Drawings and Prints": 9,
    "Egyptian Art": 10,
    "European Paintings": 11,
    "Islamic Art": 14,
}

st.sidebar.header("🔍 Search Options")
department = st.sidebar.selectbox("Choose Department", list(departments.keys()))
query = st.sidebar.text_input("Enter search keyword (e.g., 'Monet', 'Sculpture')")

# --- Search button ---
if st.sidebar.button("Search"):
    dept_id = departments[department]
    st.write(f"Searching for: **{query}** in department: **{department}**")
    object_ids = search_artworks(query, dept_id)
    if object_ids:
        st.write(f"Found {len(object_ids)} artworks.")
        # Display first few results
        for obj_id in object_ids[:5]:
            artwork = get_artwork_details(obj_id)
            if artwork and artwork.get("primaryImageSmall"):
                st.image(artwork["primaryImageSmall"], caption=artwork["title"])
                st.write(f"**Artist:** {artwork.get('artistDisplayName', 'Unknown')}")
                st.write(f"**Date:** {artwork.get('objectDate', 'N/A')}")
                st.write(f"**Medium:** {artwork.get('medium', 'N/A')}")
                st.write("---")
    else:
        st.warning("No results found.")

# --- Random artwork button ---
if st.sidebar.button("🎲 Random Artwork"):
    st.subheader("Random Artwork")
    artwork = random_artwork()
    if artwork and artwork.get("primaryImageSmall"):
        st.image(artwork["primaryImageSmall"], caption=artwork["title"])
        st.write(f"**Artist:** {artwork.get('artistDisplayName', 'Unknown')}")
        st.write(f"**Date:** {artwork.get('objectDate', 'N/A')}")
        st.write(f"**Medium:** {artwork.get('medium', 'N/A')}")
    else:
        st.warning("No image found.")
