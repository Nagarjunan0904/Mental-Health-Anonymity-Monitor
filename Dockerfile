

FROM python:3.11-slim

# set working directory
WORKDIR /app

# install only the allowed lightweight library
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source code
COPY . .

# make sure the database is written to a persistent volume
VOLUME ["/app/data"]

# default command runs the collector continuously
ENTRYPOINT ["bash", "entrypoint.sh"]
