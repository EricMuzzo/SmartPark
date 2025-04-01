FROM python:3.13.2-slim
ENV TZ="America/New_York"

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip==25.0.1
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 80
EXPOSE 8080

CMD ["python", "simulator.py"]