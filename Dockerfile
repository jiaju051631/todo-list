FROM python:3-alpine3.15
WORKDIR /todo-list
COPY . /todo-list
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py