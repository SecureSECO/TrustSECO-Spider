FROM python:3.10.4-slim

WORKDIR /app

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN apt-get update && apt-get install -y \
    clamav-daemon \
    wget \
    socat \
    && rm -rf /var/lib/apt/lists/*

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]


# This program has been developed by students from the bachelor Computer Science at Utrecht University within the Software Project course.
# © Copyright Utrecht University (Department of Information and Computing Sciences)
