import streamlit as st
import pandas as pd
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="Global Premier League", layout="wide")

# --- Google Sheets Setup ---
SHEET_NAME = "Global Premier League"
WORKSHEET_NAME = "Sheet1"

@st.cache_resource
def get_worksheet():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "global-premier-league-56becf780ee6.json", scope
    )
    client = gspread.authorize(creds)
    sheet = client.open(SHEET_NAME)
    return sheet.worksheet(WORKSHEET_NAME)

worksheet = get_worksheet()

# --- Load Data from Google Sheets ---
@st.cache_data(ttl=60)
def load_data():
    try:
        data = worksheet.get_all_records()
        return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(columns=["Name", "Team", "Sales Type", "Runs", "Sales Amount", "Date"])

df = load_data()

# --- Constants ---
teams = {
    "Charles United": ["Fahad", "Charlotte", "Parameshwari", "Arpita", "Harsh", "Shailja"],
    "Laimina Falcons": ["Zunaira", "Anushka", "Jhalak", "Farman", "Gurjeet", "Laxmi"],
}
player_team_map = {player: team for team, players in teams.items() for player in players}
all_players = [p for players in teams.values() for p in players]
run_values = {"Full-Time": 100, "Part-Time": 50, "Hourly": 25}

# --- Scoreboard Heading ---
st.markdown("""
    <h1 style='text-align: center;'>🎉🏏 Global Premier League Scoreboard 🏏🎉</h1>
    <h4 style='text-align: center; color: grey;'>Tournament Dates: April 14 - May 14</h4>
""", unsafe_allow_html=True)

# --- Color player names by team ---
def color_player_name(name):
    team = player_team_map.get(name)
    if team == "Charles United":
        return f'<span style="color:green">{name}</span>'
    elif team == "Laimina Falcons":
        return f'<span style="color:blue">{name}</span>'
    return name

# --- Handle empty data ---
if df.empty or "Name" not in df.columns:
    st.warning("No data available yet. Add a sale to get started!")
    top_scorers = pd.DataFrame(columns=["Name", "Runs", "Sales Amount"])
    team_standings = pd.DataFrame(columns=["Team", "Runs", "Sales Amount"])
    charles_runs = laimina_runs = total_runs = total_sales = 0
else:
    # --- Top Scorers ---
    top_scorers = (
        df.groupby("Name")
        .agg({"Runs": "sum", "Sales Amount": "sum"})
        .sort_values("Runs", ascending=False)
        .reset_index()
    )
    top_scorers["Name"] = top_scorers["Name"].apply(color_player_name)

    # --- Team Standings ---
    team_standings = (
        df.groupby("Team")
        .agg({"Runs": "sum", "Sales Amount": "sum"})
        .sort_values("Runs", ascending=False)
        .reset_index()
    )

    charles_runs = team_standings[team_standings["Team"] == "Charles United"]["Runs"].sum()
    laimina_runs = team_standings[team_standings["Team"] == "Laimina Falcons"]["Runs"].sum()

    total_runs = df["Runs"].sum()
    total_sales = df["Sales Amount"].sum()

# --- Top Scorers Display ---
st.markdown("## 🥇 Top Scorers")
st.write(top_scorers.to_html(escape=False, index=False, classes="styled-table"), unsafe_allow_html=True)

# --- Team Standings Display ---
st.markdown("## 🏆 Team Standings")
st.write(team_standings.to_html(index=False, classes="styled-table"), unsafe_allow_html=True)

# --- Team Run Totals ---
st.markdown(f"""
<div style='display: flex; justify-content: center; gap: 80px; font-size: 24px;'>
    <div style='text-align: center;'>
        <b>Charles United</b><br>
        <span style='color:green; font-size: 32px;'>🏏 {charles_runs}</span>
    </div>
    <div style='text-align: center;'>
        <b>Laimina Falcons</b><br>
        <span style='color:blue; font-size: 32px;'>🏏 {laimina_runs}</span>
    </div>
</div>
<br>
""", unsafe_allow_html=True)

# --- Totals ---
col1, col2 = st.columns(2)
col1.metric("Total Runs 🏏", total_runs)
col2.metric("Total Sales 💰", f"${total_sales:,.2f}")

# --- Legend ---
st.markdown("<p style='text-align: center;'>Runs: 💯 (Full-Time) | 𝟱𝟬 (Part-Time) | 𝟮𝟱 (Hourly)</p><hr>", unsafe_allow_html=True)

# --- CSS Styling ---
st.markdown("""
<style>
.styled-table {
    border-collapse: collapse;
    width: 100%;
    margin: 0 auto;
    font-size: 16px;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
}
.styled-table thead tr {
    background-color: #007bff;
    color: #ffffff;
    text-align: left;
}
.styled-table th, .styled-table td {
    padding: 12px 15px;
}
.styled-table tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}
.styled-table tbody tr:last-of-type {
    border-bottom: 2px solid #007bff;
}
</style>
""", unsafe_allow_html=True)

# --- Admin Section: Submit a Sale ---
with st.expander("🔐 Admin: Submit a Sale"):
    with st.form("sales_form"):
        name = st.selectbox("Salesperson", all_players)
        sale_type = st.selectbox("Type of Client", list(run_values.keys()))
        sale_amount = st.number_input("💰 Sales Amount", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Submit Sale")

        if submit:
            team = player_team_map.get(name)
            runs = run_values[sale_type]
            today = str(date.today())
            row = [name, team, sale_type, runs, sale_amount, today]
            worksheet.append_row(row)
            st.cache_data.clear()
            st.success(f"✅ Sale recorded for {name} ({sale_type}) - {runs} runs, ₹{sale_amount}")
