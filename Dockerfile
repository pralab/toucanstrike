FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install -y git && apt-get install -y libmagic1

RUN git clone https://github.com/snehith57624/toucanstrike.git

# Expose the port
EXPOSE 5000

# Install Python dependencies
RUN pip install flask colorama && pip install tqdm && pip install -U "ipython>=7.20"

RUN cd toucanstrike && git pull && pip install -r requirements.txt


# Set the entrypoint command
CMD ["python3", "toucanstrike/app.py"]
