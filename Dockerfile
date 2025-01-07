FROM python:3.10-alpine3.19

LABEL source_repository="https://github.com/baonq-me/redfish-exporter"
LABEL maintainer="Quoc-Bao Nguyen <quocbao747@gmail.com>"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

ADD collectors /app/collectors
COPY *.py /app

CMD ["python3", "redfish-exporter.py"]