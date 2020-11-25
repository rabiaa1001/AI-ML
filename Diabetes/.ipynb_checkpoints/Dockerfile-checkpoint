FROM ubuntu:latest
RUN apt-get update && apt-get -y update
RUN apt-get install -y build-essential python3.7 python3-pip python3-dev
RUN pip3 -q install pip --upgrade
RUN mkdir src
WORKDIR src/
COPY . /src/
RUN pip3 install -r requirements.txt
RUN pip3 install jupyter
RUN python3 diabetes_module.py
# Add Tini. Tini operates as a process subpreaper for Jupyter. This prevents kernel crashes.
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini","--"]
EXPOSE 8888 8123
CMD ["jupyter","notebook","--port=8888","--no-browser","--ip=0.0.0.0","--allow-root"]

