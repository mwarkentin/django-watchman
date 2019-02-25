FROM python:slim
COPY . /app
WORKDIR /app/sample_project
RUN pip install --no-cache -r requirements.txt
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
