FROM python:3.10-alpine
WORKDIR /authentication
COPY . /authentication
RUN python3 -m ensurepip
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN cd auth_service
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
