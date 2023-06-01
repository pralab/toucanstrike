FROM ubuntu:latest

# Install necessary dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get update && apt-get upgrade -y && apt-get install -y git && apt-get install -y libmagic1 && apt-get install -y curl
RUN git clone https://github.com/snehith57624/toucanstrike.git
# RUN cd toucanstrike

# Expose the port
EXPOSE 5000

# Install Python dependencies
RUN pip install flask colorama && pip install tqdm && pip install -U "ipython>=7.20"
# RUN PYTHONPATH=/usr/bin/python pip install -r requirements.txt
# RUN cd toucanstrike && git checkout webserver && pip install -r requirements.txt && python3 app.py
RUN cd toucanstrike && git checkout webserver && git pull && pip install -r requirements.txt


# Set the entrypoint command
CMD ["python3", "toucanstrike/app.py"]
