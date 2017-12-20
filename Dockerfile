FROM python
COPY . /app
RUN pip install -r /app/sample_project/requirements.txt
RUN python /app/sample_project/manage.py migrate

CMD ["python", "/app/sample_project/manage.py", "runserver", "0.0.0.0:8000"]
