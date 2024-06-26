# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/JJM

# Copy the requirements file into the container at /usr/src/JJM
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Chrome and ChromeDriver for Selenium

# Update the package list
RUN apt-get update 

# Install wget, gnupg2, and unzip
RUN apt-get install -y wget gnupg2 unzip

# Download and add Google's signing key
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - 

# Add Google Chrome's repository to the sources list
RUN sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' 

# Update the package list again to include the new repository
RUN apt-get update 

# Install Google Chrome
RUN apt-get install -y google-chrome-stable 

# Download ChromeDriver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip 

# Unzip ChromeDriver and place it in /usr/local/bin
RUN unzip /tmp/chromedriver.zip -d /usr/local/bin/

# Remove the downloaded zip file
RUN rm /tmp/chromedriver.zip

# Copy the current directory contents into the container at /usr/src/JJM
COPY . .

# Set environment variable for Chrome
ENV PATH=/usr/local/bin/chromedriver:$PATH

# Command to run your scripts # CMD ["sh", "-c", "python scrapj36.py && python dashboard.py"]
CMD ["python", "scrapj36.py"]
CMD ["python", "dashboard.py"]
