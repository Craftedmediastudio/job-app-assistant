import streamlit as st
import docx2txt
import requests
from bs4 import BeautifulSoup
import tempfile

st.set_page_config(page_title="Job Application Assistant", layout="wide")
st.title("🚀 Smart Job Finder & Application Assistant")

st.markdown("Upload your CV and search for remote, part-time social media jobs.")

# 1. Upload CV
st.header("1. Upload Your CV")
cv_file = st.file_uploader("Upload your CV (DOCX format preferred)", type=["docx"])

cv_text = ""
if cv_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp:
        tmp.write(cv_file.read())
        tmp_path = tmp.name
    cv_text = docx2txt.process(tmp_path)
    st.success("CV uploaded and processed.")
    st.text_area("Extracted CV Text", cv_text, height=200)

# 2. Job Search Settings
st.header("2. Search Settings")
keywords = st.text_input("Job Keywords", value="social media manager")
location = st.text_input("Location", value="remote")
part_time_only = st.checkbox("Only show part-time/flexible jobs", value=True)

# 3. Job Scraper (Indeed)
st.header("3. Job Matches (Indeed Only - Prototype)")

def scrape_indeed(keywords, location):
    query = f"{keywords} {location}".replace(" ", "+")
    url = f"https://www.indeed.com/jobs?q={query}&fromage=3&limit=10"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for div in soup.find_all("a", href=True):
        title = div.get_text(strip=True)
        link = div.get("href")
        if not link.startswith("http"):
            link = "https://www.indeed.com" + link
        if title:
            results.append({"title": title, "link": link})
    return results

if st.button("Search Jobs") and cv_text:
    st.info("Searching for jobs...")
    job_results = scrape_indeed(keywords, location)
    if not job_results:
        st.error("No jobs found. Try changing your keywords or location.")
    selected_jobs = []
    for idx, job in enumerate(job_results):
        if st.checkbox(f"{job['title']}", key=idx):
            selected_jobs.append(job)

    if selected_jobs:
        st.markdown("---")
        st.subheader("4. Review & Prepare Applications")
        for job in selected_jobs:
            st.write(f"**{job['title']}**")
            st.write(f"[View Job Posting]({job['link']})")
            st.text_area(
                "Auto-filled Cover Letter (example)",
                f"Dear Hiring Team,\n\nI am excited to apply for the role of {job['title']}.\n\nRegards,\nJane Mitchell"
            )
elif not cv_text:
    st.warning("Please upload your CV before searching for jobs.")
