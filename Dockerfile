FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/
ENV REDIS_URL=redis://redis:6379/1
EXPOSE 8000
CMD ["gunicorn", "gestion_empresas.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
