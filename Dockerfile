FROM python:3.11.6

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY commonwealth-bank-logo-png-icon-diamond-300x300.png .

COPY main.py .

EXPOSE 8501
CMD ["streamlit", "run", "main.py"]