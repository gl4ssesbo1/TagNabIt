FROM python:3.10

WORKDIR /tagnabit
COPY . .

ADD ./output /tagnabit/output

RUN apt update && apt install python3-pip -y
RUN python3 -m pip install -r requirements.txt

ENTRYPOINT ["python3", "TagNabIt.py"]
