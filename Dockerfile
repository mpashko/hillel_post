FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add --no-cache gcc alpine-sdk python3-dev jpeg-dev zlib-dev musl-dev libffi-dev libressl-dev cargo postgresql-libs postgresql-dev

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]