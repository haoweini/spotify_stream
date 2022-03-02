FROM python:3.8

COPY src /app/src
COPY requirements.txt /app

RUN mkdir -p /app/data/raw

COPY data/raw/spotify_creds.json /app/data/raw
COPY data/raw/spotify_token.json /app/data/raw
COPY data/raw/me.jpg /app/data/raw
COPY data/raw/user_pic.jpg /app/data/raw

# Make base or working directory 
WORKDIR /app

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app/src

RUN python get_token.py
COPY data/raw/spotify_token.json /app/data/raw

# Google cloud app engine by default run on port 8080
# --server.enableCORS false is for google cloud

#CMD python get_token.py 
#CMD streamlit run --server.port 8503 app.py
CMD streamlit run --server.port 8080 --server.enableCORS false  --server.enableXsrfProtection false app.py
