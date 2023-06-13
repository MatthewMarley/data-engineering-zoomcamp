# base image
FROM python:3.9

RUN pip install pandas

WORKDIR /app
COPY pipeline.py pipeline.py

# Override python entry point. Replace with bash entrypoint
ENTRYPOINT [ "bash" ]

