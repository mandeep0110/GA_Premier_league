# Global Premier League (GPL) Scoreboard App

This repository contains a Streamlit application that displays a live scoreboard for the Global Premier League (GPL). The app tracks team and player scores, sales data, and provides an admin panel for updating the scoreboard.

## Features

* **Scoreboard Display:**
    * Displays the top scorers with their runs and sales amounts.
    * Shows team standings with total runs and sales amounts.
    * Provides a visual comparison of runs between "Charles United" and "Laimina Falcons".
* **Data Source:** The app reads sales data from a `sales_data.csv` file.
* **Admin Panel:**
    * Allows authorized users to submit new sales records.
    * Records the player, sale type, sales amount, and date of the sale.
    * Updates the `sales_data.csv` file with new entries.
* **Layout and Styling:**
    * The app is built using Streamlit and includes custom styling.
    * The  Top Scorers and Team standings are displayed in parallel.

## Requirements

The application requires the following Python libraries:

* **streamlit**:  The core library for creating the interactive web app.
* **pandas**:  A library for data manipulation, used for handling and processing the data from `sales_data.csv`.

## Data File

* `sales_data.csv`: This file stores the sales data, including player names, team, sales type, runs, sales amount, and date.  The app reads from and writes to this file.

## How to Run the App

1.  **Clone this repository.**
2.  **Ensure you have Python installed.**
3.  **Install the required libraries:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
5.  **Access the app in your browser:** Streamlit will provide a local URL (usually `http://localhost:8501`) where you can view the app.

## Admin Access

* The app includes an admin panel (within an expandable section) for submitting sales data.