# Use an official Python runtime as a parent image
FROM python:3.12-slim

LABEL org.opencontainers.image.source=https://github.com/TheItsNameless/cs24-1-bot

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV DISCORD_TOKEN=''
ENV CUR_SERVER=''
ENV MENSA_CHANNEL=''

# Run bot.py when the container launches
CMD ["python", "-u", "main.py"]