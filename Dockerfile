FROM python:3.10-alpine

COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY main.py /

EXPOSE 9991

CMD ["python3", "main.py"]
