FROM python
COPY . /app
WORKDIR /app/sample_project
RUN pip install -r requirements.txt
RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
