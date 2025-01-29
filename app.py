import streamlit as st
import requests
import base64
import time
import os


token = st.secrets["TOKEN"]

def main():
    st.title("Manual Hourly Refresh Demo")

    # 1. Track the last refresh time in session state
    if "last_refresh" not in st.session_state:
        st.session_state["last_refresh"] = time.time()

    current_time = time.time()
    # 2. If more than 3600 seconds (1 hour) has passed -> refresh
    if current_time - st.session_state["last_refresh"] > 3600:  # 1 hour
        st.session_state["last_refresh"] = current_time
        st.rerun()  # Force the app to re-run

    # 3. GitHub fetch logic
    st.write("Fetching data from GitHub...")

    # GitHub CSV file URL
    GITHUB_URL = "https://api.github.com/repos/tunghoang0182/call-daily-tracker/contents/sales_data.csv"

    headers = {"Authorization": f"token {token}"}
    response = requests.get(GITHUB_URL, headers=headers)

    if response.status_code == 200:
        content_json = response.json()
        file_content = base64.b64decode(content_json['content']).decode('utf-8')
        
        # 4. Save the file to Z:\Data\Other (Windows)
        # Make sure Z:\ is accessible and you have write permission
        local_path = r"Z:\Data\Other\sales_data.csv"
        
        try:
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(file_content)
            st.success(f"✅ File saved to: {local_path}")
        except Exception as e:
            st.error(f"Failed to save file to {local_path}\nError: {e}")

    else:
        st.error(
            f"❌ Failed to fetch file. "
            f"Status code: {response.status_code}, "
            f"Message: {response.json()}"
        )

if __name__ == "__main__":
    main()

