FROM debian:stable as base_image

RUN mkdir -p /isbonrecording
WORKDIR /isbonrecording
COPY backend/main.py /isbonrecording/
COPY backend/req.txt /isbonrecording/

RUN apt update -y && apt upgrade -y && \
    apt install -y usbutils libudev-dev python3 python3-pip python3-venv python-dev

RUN python3 -m venv .env && . /isbonrecording/.env/bin/activate && \
    pip install -U pip && pip install -r req.txt && pyinstaller --onefile main.py -n isbonrecording

FROM debian:stable as final_image
COPY --from=base_image /isbonrecording/dist/isbonrecording /usr/local/bin/

RUN apt update -y && apt upgrade -y && \
    apt install -y usbutils libudev-dev && \
    apt-get autoremove -y

WORKDIR /isbonrecording
ENTRYPOINT [ "/isbonrecording/.env/bin/python3","/isbonrecording/main.py" ]
