# IoT Predictive Maintenance

A simple Streamlit app for predicting equipment safety vs. failure risk using pre-trained models stored in `models_pkl/`. The UI offers:

- Manual Input: enter a single device's parameters and get a prediction with confidence and a gauge visualization.
- CSV Upload: batch analyze multiple records, preview results, and download a CSV of predictions.

## Features

- Clean single-page UI with helpful sidebar (no routes)
- Validation and preprocessing via `utils/data_processor.py`
- Model loading and prediction via `models/model_manager.py`
- Visual feedback: status badge + Plotly gauge

## Requirements

- Python 3.9+ recommended
- See `requirements.txt`

## Quick Start

### Linux/macOS

```bash
# From project root
chmod +x install.sh
./install.sh
```

This will:

- Create a virtual environment `.venv`
- Install dependencies
- Run the app: http://localhost:8501

### Windows (PowerShell or CMD)

```bat
install.bat
```

This will:

- Create a virtual environment `.venv`
- Install dependencies
- Run the app at http://localhost:8501

## Manual Setup

If you prefer manual steps:

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

```bat
:: Windows
python -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

## Usage

- Choose the model from the sidebar.
- Manual Input tab: fill in temperatures, `rotational_speed_rpm`, `torque_nm`, and `tool_wear_min`.
- CSV Upload tab: upload a CSV with columns:
  `air_temperature_k, process_temperature_k, rotational_speed_rpm, torque_nm, tool_wear_min`
- Download the results CSV after batch prediction.

## Troubleshooting

- If you see old pages in the sidebar, clear Streamlit cache and restart:

```bash
python -m streamlit cache clear
python -m streamlit run app.py
```

- Ensure `models_pkl/` contains the expected `.pkl` model and scaler files referenced by `models/model_manager.py`.
- If ports conflict, Streamlit allows specifying another port:

```bash
python -m streamlit run app.py --server.port 8502
```

## Project Structure

```
app.py
config.py
requirements.txt
install.sh
install.bat
models/
models_pkl/
utils/
components/
```

## License

Proprietary — internal use for IoT predictive maintenance demonstrations.
