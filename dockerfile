FROM python:3.10.13-alpine

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY req_unix.txt /app/
RUN pip install --no-cache-dir -r req_unix.txt


COPY . /app

# EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

