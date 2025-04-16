import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Global Premier League", layout="wide")

# Constants
DATA_FILE = "sales_data.csv"

# Team and Player Data
teams = {
    "Charles United": ["Fahad", "Charlotte", "Parameshwari", "Arpita", "Harsh", "Shailja"],
    "Laimina Falcons": ["Zunaira", "Anushka", "Jhalak", "Farman", "Gurjeet", "Laxmi"]
}

# Create a mapping of player to team for coloring
player_team_map = {}
for team, players in teams.items():
    for player in players:
        player_team_map[player] = team

# Combine all players into a single list
all_players = [player for sublist in teams.values() for player in sublist]

# Run values for each client type
run_values = {
    "Full-Time": 100,
    "Part-Time": 50,
    "Hourly": 25
}

# Load or create data file
@st.cache_data
def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Team", "Sales Type", "Runs", "Sales Amount", "Date"])

df = load_data()

# Scoreboard Heading
st.markdown("""
    <h1 style='text-align: center;'>🎉🏏 Global Premier League Scoreboard 🏏🎉</h1>
    <h4 style='text-align: center; color: grey;'>Tournament Dates: April 14 - May 14</h4>
""", unsafe_allow_html=True)

# --- Top Scorers and Team Standings (Parallel & Designed) ---
st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
col_top, col_team = st.columns(2)

with col_top:
    st.markdown("<h2 style='color: gold; text-align: center;'>🥇 Top Scorers</h2>", unsafe_allow_html=True)
    top_scorers = df.groupby("Name").agg({"Runs": "sum", "Sales Amount": "sum"}).sort_values("Runs", ascending=False).reset_index()
    top_scorers['Styled Name'] = top_scorers['Name'].apply(lambda name: f'<span style="color: {"green" if player_team_map.get(name) == "Charles United" else "blue" if player_team_map.get(name) == "Laimina Falcons" else "black"}">{name}</span>')
    st.write(top_scorers[['Styled Name', 'Runs', 'Sales Amount']].to_html(escape=False, index=False, classes='styled-table'), unsafe_allow_html=True)

with col_team:
    st.markdown("<h2 style='color: #4CAF50; text-align: center;'>🏆 Team Standings</h2>", unsafe_allow_html=True)
    team_standings = df.groupby("Team").agg({"Runs": "sum", "Sales Amount": "sum"}).sort_values("Runs", ascending=False).reset_index()
    st.write(team_standings.to_html(index=False, classes='styled-table'), unsafe_allow_html=True)

# --- Custom CSS for Table Styling ---
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

.styled-table th,
.styled-table td {
    padding: 12px 15px;
}

.styled-table tbody tr {
    border-bottom: 1px solid #dddddd;
}

.styled-table tbody tr:nth-of-type(even) {
    background-color: #f3f3f3;
}

.styled-table tbody tr:last-of-type {
    border-bottom: 2px solid #007bff;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)

# Team vs Team Display
charles_runs = team_standings[team_standings['Team'] == "Charles United"]["Runs"].sum() if not team_standings.empty and "Charles United" in team_standings['Team'].values else 0
laimina_runs = team_standings[team_standings['Team'] == "Laimina Falcons"]["Runs"].sum() if not team_standings.empty and "Laimina Falcons" in team_standings['Team'].values else 0

st.markdown("""
<div style='display: flex; justify-content: center; gap: 80px; font-size: 24px;'>
    <div style='text-align: center;'>
        <b>Charles United</b><br>
        <span style='color:green; font-size: 32px;'>🏏 {}</span>
    </div>
    <div style='text-align: center;'>
        <b>Laimina Falcons</b><br>
        <span style='color:blue; font-size: 32px;'>🏏 {}</span>
    </div>
</div>
<br>
""".format(charles_runs, laimina_runs), unsafe_allow_html=True)

# Total Summary
total_runs = df["Runs"].sum()
total_sales = df["Sales Amount"].sum()
col1, col2 = st.columns(2)
with col1:
    st.metric("Total Runs 🏏", total_runs)
with col2:
    st.metric("Total Sales 💰", f"${total_sales:,.2f}")

# Legend
st.markdown("""
<p style='text-align: center;'>Runs: 💯 (Full-Time) | 𝟱𝟬 (Part-Time) | 𝟮𝟱 (Hourly)</p>
<hr>
""", unsafe_allow_html=True)

# 🔐 Admin section (you can hide this with password later)
with st.expander("🔐 Admin: Submit a Sale"):
    with st.form("sales_form"):
        name = st.selectbox("Salesperson", all_players)
        sale_type = st.selectbox("Type of Client", list(run_values.keys()))
        sale_amount = st.number_input("💰 Sales Amount", min_value=0.0, format="%.2f")
        submit = st.form_submit_button("Submit Sale")

        if submit:
            team = player_team_map.get(name)
            runs = run_values[sale_type]
            new_entry = pd.DataFrame({
                "Name": [name],
                "Team": [team],
                "Sales Type": [sale_type],
                "Runs": [runs],
                "Sales Amount": [sale_amount],
                "Date": [str(date.today())]
            })
            df = pd.concat([df, new_entry], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.cache_data.clear()
            st.success(f"✅ Sale recorded for {name} ({sale_type}) - {runs} runs, ₹{sale_amount}")