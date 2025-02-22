# Container image that runs your code
FROM python:3.12-alpine

# Copies your code file from your action repository to the filesystem path `/` of the container
# COPY entrypoint.sh /entrypoint.sh

# COPY . .
COPY src/ src/
COPY requirements.txt /requirements.txt
COPY designite_util-1.0.0.tar.gz /designite_util-1.0.0.tar.gz
RUN pip install -r requirements.txt
RUN pip install designite_util-1.0.0.tar.gz

#RUN ls -a
#RUN ls -a src/

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["python", "/src/main.py"]