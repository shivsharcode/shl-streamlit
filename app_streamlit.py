import streamlit as st
import pandas as pd
import requests

# set API ENDPOINT
API_URL = "https://shl-backend-api-1.onrender.com/recommend"

st.set_page_config(page_title = "SHL Assessment Recommender", layout="wide")

st.title("🔍 SHL Assessment Recommendation Engine")
st.markdown("Enter a job requirement or query to get the most relevant SHL assessments.")

# ---------FORM INPUTS------------
with st.form("query_form"):
    query = st.text_input("Query", placeholder="e.g. Looking for Python assessment under 45 minutes")
    # top_k = st.slider("Number of Recommendations", min_value=1, max_value=10, value=10)
    submit = st.form_submit_button("🔎 Recommend")
    

# ---------QUERY BACKEND----------
if submit:
    if not query.strip():
        st.warning("Please enter a valid query.")
    else:
        with st.spinner("Fetching recommendations"):
            try:
                res = requests.post(API_URL, json={
                    "query": query,
                })
                res.raise_for_status() # checks if the req encountered an error(like 404 or 500), If the req fails it raises an exception rather than silently failing
                results = res.json()["results"]
                
                if not results:
                    st.info("No recommendations found")
                else:
                    # FORMAT TO A TABLE
                    data = []
                    for r in results:
                        data.append({
                            "Name": f"{[{r['url'].split('/')[-2].replace('-', ' ').title() }][0]} ",
                            # "Name2": r['name'],
                            "URL": r['url'],
                            "Duration (min)": r['duration'],
                            "Adaptive": r["adaptive_support"],
                            "Remote": r["remote_support"],
                            "Test_types": ", ".join(r['test_types']),
                            # "Score": f"{r['cosine_similarity_score']:.3f}",
                            "Description": r['description'],
                        })
                        
                    df = pd.DataFrame(data)
                    st.markdown("### 🔗 Recommended Assessments")
                    st.dataframe(df, use_container_width=True)
            
            except Exception as e:
                st.error(f"Failed to connect to API {e}")