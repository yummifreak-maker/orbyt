import os
import sqlite3
import pandas as pd
import streamlit as st
from datetime import datetime
from config import Config
from scraper import JobScraper
from tailor import ProfileTailor

# Page Setup
st.set_page_config(page_title="Orbyt - Quant Job Workspace", page_icon="🚀", layout="wide")

def init_workspace_db():
    conn = sqlite3.connect("orbyt_workspace.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS workspace (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            post_name TEXT,
            jd_link TEXT,
            cover_letter TEXT,
            status TEXT DEFAULT 'Staged for Review'
        )
    ''')
    conn.commit()
    conn.close()

init_workspace_db()

# Sidebar Control Center
if os.path.exists("orbyt_logo.png"):
    st.sidebar.image("orbyt_logo.png", use_container_width=True)
else:
    st.sidebar.markdown("### 🚀 Orbyt")

st.sidebar.title("Orbyt Control Center")
st.sidebar.markdown(f"**Target:** Quant Roles (US)")
st.sidebar.markdown(f"**Authorization:** F-1 STEM OPT (Jul 2028)")
st.sidebar.markdown(f"**Email:** `{Config.USER_EMAIL}`")

if st.sidebar.button("🔍 Run Scraper & Stage Jobs"):
    with st.spinner("Scanning Google Jobs & Boards for matching quantitative roles..."):
        scraper = JobScraper()
        tailor = ProfileTailor()
        jobs = scraper.search_jobs()
        
        conn = sqlite3.connect("orbyt_workspace.db")
        cursor = conn.cursor()
        for job in jobs:
            c_name = job["company"]
            p_name = job["title"]
            j_link = job["link"]
            cl_text = tailor.generate_cover_letter(c_name, p_name, "")
            
            cursor.execute('''
                INSERT INTO workspace (company_name, post_name, jd_link, cover_letter, status)
                VALUES (?, ?, ?, ?, 'Staged for Review')
            ''', (c_name, p_name, j_link, cl_text))
        conn.commit()
        conn.close()
    st.sidebar.success("New positions successfully staged!")

# Main Dashboard Interface
st.title("Orbyt: Discover | Apply | Track | Succeed")
st.markdown("Manual qualification workspace. Review matching quantitative positions, inspect human-like cover letters, and track application states locally.")

# Fetch Database Records
conn = sqlite3.connect("orbyt_workspace.db")
df = pd.read_sql("SELECT * FROM workspace", conn)
conn.close()

if df.empty:
    st.info("No jobs staged yet. Use the sidebar button **'Run Scraper & Stage Jobs'** to begin.")
else:
    tab1, tab2 = st.tabs(["📋 Staged Review Queue", "📊 Tracking Dashboard"])
    
    with tab1:
        st.subheader("Staged Roles Requiring Manual Evaluation")
        for index, row in df.iterrows():
            with st.expander(f"{row['company_name']} — {row['post_name']} ({row['status']})"):
                st.markdown(f"**Job Link:** [Open Description]({row['jd_link']})")
                st.markdown("**Tailored Human-Like Cover Letter:**")
                st.text_area("Cover Letter", row['cover_letter'], height=200, key=f"cl_{row['id']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Mark as Qualified / Ready", key=f"qual_{row['id']}"):
                        conn = sqlite3.connect("orbyt_workspace.db")
                        cursor = conn.cursor()
                        cursor.execute("UPDATE workspace SET status = 'Qualified (Manual)' WHERE id = ?", (row['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()
                with col2:
                    if st.button("Discard Position", key=f"disc_{row['id']}"):
                        conn = sqlite3.connect("orbyt_workspace.db")
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM workspace WHERE id = ?", (row['id'],))
                        conn.commit()
                        conn.close()
                        st.rerun()

    with tab2:
        st.subheader("Application Tracking Matrix")
        st.dataframe(df[["id", "company_name", "post_name", "jd_link", "status"]], use_container_width=True)