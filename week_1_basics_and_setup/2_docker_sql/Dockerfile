# Set the base image to use (Used interchangably with parent)
FROM python:3.9

# Using python:3.9 as the base image
# Install pandas into the base image
# This will modify the parent image
RUN pip install pandas

# Where we want to copy the below file to when creating the image
# Creates app folder from root directory
WORKDIR /app

# Name of script to copy from source -> to destination
COPY pipeline.py pipeline.py

# Will run on run -it. If no CLI arg then today's date. Else CLI arg[1]
ENTRYPOINT [ "python", "pipeline.py" ]

# ENTRYPOINT ["bash"]  <-- Original entrypoint
