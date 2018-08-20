# Dockerfile
FROM python:3.6

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create app directory
# RUN mkdir -p /app
RUN mkdir -p /app
WORKDIR /app

COPY . /app
COPY manage.py requirements.txt /app/
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]