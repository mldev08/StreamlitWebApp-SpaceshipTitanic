FROM python:3.10s
EXPOSE 8501
WORKDIR /app
COPY . .
RUN python -m pip install -r requirements.txt


CMD streamlit run app.py \
    --server.headless true \
    --browser.serverAddress="0.0.0.0" \
    --server.enableCORS false \
    --browser.gatherUsageStats false
