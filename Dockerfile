FROM python
COPY . /app
RUN pip install "django<1.9"
RUN pip install -e /app
RUN python /app/sample_project/manage.py migrate

CMD ["python", "/app/sample_project/manage.py", "runserver", "0.0.0.0:8000"]
