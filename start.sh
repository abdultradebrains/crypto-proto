#!/bin/bash

# Run Python script in the background
python websocket/runner.py &

# Run Streamlit app in the foreground
exec streamlit run app.py --server.port 8501 --server.address 0.0.0.0