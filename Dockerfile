FROM python:3.8

COPY src /app/src
COPY requirements.txt /app

RUN mkdir -p /app/data/raw

COPY data/raw/spotify_creds.json /app/data/raw

# Make base or working directory 
WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app/src

# Google cloud app engine by default run on port 8080
# --server.enableCORS false is for google cloud
CMD streamlit run app3.py --server.port 8503