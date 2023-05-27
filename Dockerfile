FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install git
RUN git clone https://github.com/snehith57624/toucanstrike.git
RUN cd toucanstrike

# Install Python dependencies
RUN pip install -r requirements.txt
RUN pip install flask colorama

# Expose the port
EXPOSE 5000

# Set the entrypoint command
CMD ["python3", "/app.py"]
