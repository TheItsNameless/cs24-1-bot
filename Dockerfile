# Use an official Python runtime as a parent image
FROM  --platform=linux/arm64 python:3.10-slim

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
CMD ["python", "main.py"]