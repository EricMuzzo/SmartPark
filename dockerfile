FROM python:3.13.2-slim
ENV TZ="America/New_York"

WORKDIR /ui

COPY ./requirements.txt /ui/requirements.txt

RUN pip install --upgrade pip==25.0.1
RUN pip install --no-cache-dir -r /ui/requirements.txt

COPY ./app /ui/app

EXPOSE 80
ENV PYTHONUNBUFFERED=True

CMD ["python", "app/main.py"]