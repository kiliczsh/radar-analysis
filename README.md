# Technology Radar Analysis

This Streamlit app analyzes technologies from the Thoughtworks Technology Radar, providing insights into technology trends across different volumes.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/kiliczsh/radar-analysis.git
   cd radar-analysis
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the App

1. Ensure you're in the project directory and your virtual environment is activated (if you created one).

2. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

3. The app should open in your default web browser. If it doesn't, you can access it by navigating to the URL shown in the terminal (usually `http://localhost:8501`).

## Data

The app uses a `data.json` file in the project root directory. Make sure this file is present and contains the Thoughtworks Technology Radar data in the correct format.

## Features

- Interactive selection of volume range for analysis
- Filterable table of technologies
- Statistics by volume
- Charts showing technology distribution by quadrant and ring
- New vs. existing technologies chart
- List of technology occurrences with customizable minimum occurrence filter

## Author

This app was created by Muhammed Kılıç for the 8th Devnot Developer Summit on October 12, 2024.

For more information, visit [summit.devnot.com](https://summit.devnot.com/)

## Contact

- Website: [muhammedkilic.com](https://muhammedkilic.com)
- LinkedIn: [muhammedkilic](https://www.linkedin.com/in/muhammedkilic/)
- Twitter: [@kiliczsh](https://twitter.com/kiliczsh)