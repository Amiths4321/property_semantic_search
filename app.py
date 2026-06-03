import streamlit as st
import pandas as pd
import numpy as np
import faiss
import pickle
import os
from sentence_transformers import SentenceTransformer

# ---- Page Config ----
st.set_page_config(page_title="Property Semantic Search", page_icon="🔍", layout="wide")
st.title("🔍 Property Semantic Search Engine")
st.write("Search naturally — AI understands meaning, not just keywords.")

# ---- Constants ----
MODEL_NAME  = "all-MiniLM-L6-v2"   # fast, free, runs on laptop
INDEX_FILE  = "property_index.faiss"
DATA_FILE   = "properties.csv"

# ---- Load Embedding Model ----
@st.cache_resource
def load_model():
    return SentenceTransformer(MODEL_NAME)

# ---- Load & Index Properties ----
@st.cache_resource
def load_and_index(csv_path):
    df = pd.read_csv(csv_path)

    # Combine all fields into one searchable text per property
    df["search_text"] = (
        df["title"].fillna("") + " " +
        df["location"].fillna("") + " " +
        df["property_type"].fillna("") + " " +
        df["bedrooms"].astype(str) + " bedroom " +
        df["area_sqft"].astype(str) + " sqft " +
        "price " + df["price_lakhs"].astype(str) + " lakhs " +
        df["amenities"].fillna("") + " " +
        df["description"].fillna("")
    )

    model       = load_model()
    embeddings  = model.encode(df["search_text"].tolist(), show_progress_bar=False)
    embeddings  = np.array(embeddings).astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(embeddings)

    # Build FAISS index
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)   # Inner Product = cosine similarity after normalize
    index.add(embeddings)

    return df, index, model

# ---- Load Data ----
if not os.path.exists(DATA_FILE):
    st.error(f"'{DATA_FILE}' not found. Please add it to the project folder.")
    st.stop()

with st.spinner("Loading and indexing properties..."):
    df, index, model = load_and_index(DATA_FILE)
    st.success(f"✅ {len(df)} properties indexed and ready to search!")

# ---- Search Interface ----
st.markdown("---")
st.subheader("🔎 Search Properties")

# Example searches
st.write("**Try these searches:**")
examples = [
    "3 bedroom near school under 65 lakhs",
    "affordable flat for IT professional",
    "luxury property with pool",
    "investment plot with high appreciation",
    "senior citizen friendly ground floor",
    "student accommodation near college"
]

cols = st.columns(3)
for i, ex in enumerate(examples):
    if cols[i % 3].button(ex, key=f"ex_{i}"):
        st.session_state.search_query = ex

# Search box
query = st.text_input(
    "Describe what you are looking for",
    value=st.session_state.get("search_query", ""),
    placeholder="e.g. 3BHK near school under 60 lakhs in Pune"
)

# Filters
st.subheader("🎛️ Filters (Optional)")
col1, col2, col3, col4 = st.columns(4)

with col1:
    max_price = st.slider("Max Price (Lakhs)", 10, 500, 500)
with col2:
    min_beds  = st.selectbox("Min Bedrooms", [0, 1, 2, 3, 4], index=0)
with col3:
    prop_type = st.multiselect("Property Type",
        ["Apartment", "Villa", "Plot", "Row House", "Penthouse"],
        default=[]
    )
with col4:
    top_k = st.slider("Results to show", 3, 15, 5)

# ---- Search Function ----
def semantic_search(query_text, top_k=5):
    query_vec = model.encode([query_text]).astype("float32")
    faiss.normalize_L2(query_vec)
    scores, indices = index.search(query_vec, top_k * 3)  # get more, filter after

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < len(df):
            row = df.iloc[idx].copy()
            row["similarity_score"] = round(float(score) * 100, 1)
            results.append(row)

    return pd.DataFrame(results)

# ---- Run Search ----
if st.button("🔍 Search") and query:

    with st.spinner("Searching..."):
        results = semantic_search(query, top_k * 3)

        # Apply filters
        results = results[results["price_lakhs"] <= max_price]
        results = results[results["bedrooms"] >= min_beds]
        if prop_type:
            results = results[results["property_type"].isin(prop_type)]

        results = results.head(top_k)

    if results.empty:
        st.warning("No properties found. Try relaxing your filters.")
    else:
        st.success(f"Found {len(results)} matching properties")
        st.markdown("---")

        for _, row in results.iterrows():
            score_color = "🟢" if row["similarity_score"] > 70 else "🟡" if row["similarity_score"] > 50 else "🔴"

            with st.container():
                col_main, col_score = st.columns([4, 1])

                with col_main:
                    st.subheader(f"🏠 {row['title']}")
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("💰 Price",    f"₹{row['price_lakhs']} L")
                    c2.metric("🛏️ Beds",     row['bedrooms'] if row['bedrooms'] > 0 else "N/A (Plot)")
                    c3.metric("📐 Area",     f"{row['area_sqft']} sqft")
                    c4.metric("📍 Location", row['location'])

                    st.write(f"**Type:** {row['property_type']}  |  **Amenities:** {row['amenities']}")
                    st.write(f"_{row['description']}_")

                with col_score:
                    st.metric(f"{score_color} Match", f"{row['similarity_score']}%")

                st.markdown("---")

        # Show as table too
        with st.expander("📊 View as Table"):
            display_cols = ["title", "location", "bedrooms", "area_sqft", "price_lakhs", "property_type", "similarity_score"]
            st.dataframe(results[display_cols].rename(columns={
                "title": "Property",
                "location": "Location",
                "bedrooms": "Beds",
                "area_sqft": "Area (sqft)",
                "price_lakhs": "Price (L)",
                "property_type": "Type",
                "similarity_score": "Match %"
            }), use_container_width=True)

        # Download results
        st.download_button(
            "📥 Download Results (CSV)",
            data=results.to_csv(index=False),
            file_name="search_results.csv",
            mime="text/csv"
        )

# ---- Add New Property ----
st.markdown("---")
with st.expander("➕ Add a New Property to the Index"):
    st.write("Add a property and it becomes searchable immediately.")
    n_title    = st.text_input("Title")
    n_location = st.text_input("Location")
    n_type     = st.selectbox("Type", ["Apartment", "Villa", "Plot", "Row House", "Penthouse"])
    n_beds     = st.number_input("Bedrooms", 0, 10, 2)
    n_area     = st.number_input("Area (sqft)", 100, 10000, 1000)
    n_price    = st.number_input("Price (Lakhs)", 1, 1000, 50)
    n_amenities = st.text_input("Amenities")
    n_desc     = st.text_area("Description")

    if st.button("➕ Add Property"):
        if n_title and n_location and n_desc:
            new_row = {
                "id": len(df) + 1,
                "title": n_title, "location": n_location,
                "area_sqft": n_area, "bedrooms": n_beds,
                "bathrooms": 1, "price_lakhs": n_price,
                "property_type": n_type, "amenities": n_amenities,
                "description": n_desc
            }
            new_df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            new_df.to_csv(DATA_FILE, index=False)
            st.success("✅ Property added! Restart the app to include it in search.")
        else:
            st.warning("Please fill in title, location and description.")

st.markdown("---")
st.caption("Semantic Search powered by sentence-transformers + FAISS | Runs 100% on your laptop | No GPU needed")