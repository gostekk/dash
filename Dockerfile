FROM python:3.8

# Set main folder
WORKDIR /app

# Copy requirements and install pip dependencies
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copy data
ADD . /app

RUN chmod +x /app/entrypoint.sh
RUN chmod -R 755 /app

CMD [ "/app/entrypoint.sh" ]
