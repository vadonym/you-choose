FROM alpine:edge

RUN apk add --update py-pip

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt

COPY *.py /usr/src/app/

EXPOSE 5000

CMD ["python3", "/usr/src/app/app.py"]
