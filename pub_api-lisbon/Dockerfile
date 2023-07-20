FROM python:3.9.9-slim-buster
LABEL maintainer="Yann Feunteun <yann.feunteun@protonmail.com>"

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip	
RUN pip install -r requirements.txt

COPY ./ /app/

EXPOSE 8000

# command to run on container start
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload" ]