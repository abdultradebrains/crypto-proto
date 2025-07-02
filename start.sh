#!/bin/bash
python websocket/runner.py
# Run app.py in foreground
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
