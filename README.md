# 🔍 Property Semantic Search Engine
> Search properties naturally — AI understands meaning, not just keywords.
> Built with sentence-transformers + FAISS + Pandas + Streamlit. Runs 100% on your laptop. No GPU needed.

---

## 🧠 What Makes This Different

| Normal Search | Semantic Search (This Project) |
|---|---|
| Searches exact words | Understands meaning |
| "3BHK Wakad" → only finds "3BHK Wakad" | "3 bedroom near school" → finds all matching listings |
| Misses synonyms | Understands "flat" = "apartment" = "unit" |
| No context understanding | Understands budget, location intent, amenity needs |

---

## 📌 What It Does

- Upload or use your property listings CSV
- Type any natural language query — e.g. *"affordable 2BHK for IT professional near metro"*
- AI finds the best matching properties by **meaning**, not keyword
- Filter by price, bedrooms, property type
- Download results as CSV
- Add new properties to the index on the fly

---

## 🗂️ Project Structure

```
property_semantic_search/
│
├── app.py                  ← Main Streamlit app
├── properties.csv          ← Property listings data
├── requirements.txt        ← Python dependencies
└── README.md               ← This file
```

---

## ⚙️ Requirements

- Python 3.9 or above
- VS Code
- Internet connection (first run only — to download embedding model ~90MB)
- No GPU needed — runs entirely on CPU

---

## 🚀 Setup Guide

**1. Create project folder**
```bash
mkdir property_semantic_search
cd property_semantic_search
```

**2. Install dependencies**
```bash
pip install streamlit pandas faiss-cpu sentence-transformers numpy openpyxl
```

**3. Add your `properties.csv`**

Your CSV must have these columns:
```
id, title, location, area_sqft, bedrooms, bathrooms,
price_lakhs, property_type, amenities, description
```

A sample file with 15 Pune/Mumbai properties is included to get started.

**4. Run the app**
```bash
streamlit run app.py
```

App opens at → `http://localhost:8501`

On first run, the embedding model (`all-MiniLM-L6-v2`, ~90MB) downloads automatically. After that it loads instantly from cache.

---

## 🖥️ How to Use

**Search naturally:**

| What you type | What AI finds |
|---|---|
| `3 bedroom near school under 65 lakhs` | 3BHK listings with school proximity within budget |
| `affordable flat for IT professional` | Budget apartments near IT parks |
| `luxury property with pool` | Villas, penthouses with pool amenity |
| `investment plot high appreciation` | Plots in growth corridors |
| `senior citizen friendly ground floor` | Ground floor flats near hospitals |
| `student accommodation near college` | Budget 1BHK near universities |

**Filters available:**
- Max Price (Lakhs)
- Minimum Bedrooms
- Property Type (Apartment, Villa, Plot, Row House, Penthouse)
- Number of results to show

**Add new properties** using the form at the bottom — they become searchable after restart.

---

## 🔬 How It Works (Simply)

```
Your property descriptions
         ↓
sentence-transformers converts each to 384 numbers (embedding)
         ↓
FAISS stores all embeddings in a fast index
         ↓
You type: "3 bedroom near school under 60 lakhs"
         ↓
Your query is also converted to 384 numbers
         ↓
FAISS finds properties whose numbers are closest to your query
         ↓
Results ranked by similarity % — shown on screen
```

The magic: properties don't need to contain your exact words. "School nearby" and "reputed educational institute walking distance" both match "near school" because their **meaning** is similar.

---

## 📊 Sample Output

```
Search: "3 bedroom near school under 65 lakhs"

🟢 3BHK Gated Society Hadapsar    — 87% match — ₹61L  — school inside campus
🟢 Spacious 3BHK Wakad            — 84% match — ₹58L  — school nearby
🟡 3BHK Near Hospital Kothrud     — 76% match — ₹72L  — mentions schools in description
🟡 Row House Aundh                 — 61% match — ₹95L  — 3 beds but over budget
🔴 2BHK Near IT Park               — 43% match — ₹48L  — only 2 bedrooms
```

Match Score Guide:
- 🟢 70%+ = Strong match
- 🟡 50–70% = Moderate match
- 🔴 Below 50% = Weak match

---

## 🧩 Tech Stack

| Tool | Role | Cost |
|---|---|---|
| `sentence-transformers` | Converts text to embeddings | Free |
| `all-MiniLM-L6-v2` | Embedding model (90MB) | Free |
| `FAISS` | Fast similarity search (by Meta) | Free |
| `Pandas` | Load and manage CSV data | Free |
| `Streamlit` | Web UI | Free |

**Total cost to run: ₹0**

---

## 📁 properties.csv Format

```csv
id,title,location,area_sqft,bedrooms,bathrooms,price_lakhs,property_type,amenities,description
1,Spacious 3BHK Wakad,Wakad Pune,1450,3,2,58,Apartment,"School, Park, Gym","3BHK near top schools..."
2,2BHK Hinjewadi,Hinjewadi Pune,950,2,1,42,Apartment,"IT Park, Metro","Ideal for IT professionals..."
```

You can export your listings from Excel as CSV and load directly.

---

## 🔮 Upgrade Ideas

- [ ] Connect to live property database instead of CSV
- [ ] Add map view using `folium` or `pydeck`
- [ ] WhatsApp bot integration — buyer sends message → bot searches and replies
- [ ] Multi-language search (Hindi, Marathi queries)
- [ ] Image search — upload a property photo → find similar listings
- [ ] Bulk buyer-to-listing matching (upload 100 buyer requirements → auto-match)

---

## 💼 Business Applications

| Use Case | Value |
|---|---|
| Real estate website | Replace basic keyword search |
| Agent tool | Instantly match buyer brief to listings |
| Developer sales office | Staff finds matching plots in seconds |
| Bulk matching | Auto-match buyer requirements to inventory |
| WhatsApp chatbot | Buyer describes in natural language → bot replies with matches |

Sell as a service to real estate agencies for ₹3,000–10,000/month.

---

## 🛠️ Troubleshooting

**Model download slow on first run**
Normal — `all-MiniLM-L6-v2` is ~90MB. Downloads once, cached forever after.

**`faiss-cpu` install fails**
```bash
pip install faiss-cpu --no-cache-dir
```

**CSV not found error**
Make sure `properties.csv` is in the same folder as `app.py`.

**Results seem irrelevant**
Make sure your `description` column has rich text — the more detail, the better the search quality.

---

## 👤 Author

**Amit Chincholkar**
BE | MBA | 14+ years in Real Estate, Retail, Digital Marketing, IT & AI

---

## 📄 License

MIT License — free to use, modify, and sell.
