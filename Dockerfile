FROM python:3.9-slim-buster
WORKDIR /app
COPY . /app

RUN apt update -y && apt install awscli -y
RUN pip install -r requirements.txt


CMD ["python3","app.py"]

# docker build -t studentperformance   .
# docker run -p 9000:9000 studentperformance create containers
# docker login
# docker tag name1 name 2 
# docker ps ( containers)
# docker iamges ( docker iamges)
# docker push brini123/studentperformance
# Docker compose ( run multiple containers)
