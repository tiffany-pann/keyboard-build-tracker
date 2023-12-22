FROM python:3.10.9

RUN mkdir usr/app
WORKDIR usr/app

COPY . .

RUN pip3 install -r requirements.txt

## determines which app you want to run when the docker file is ran
CMD ["python3", "app.py"]