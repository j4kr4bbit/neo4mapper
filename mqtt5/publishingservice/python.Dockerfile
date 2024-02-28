FROM python:3.9
COPY publisher.py /publisher.py
RUN pip install paho-mqtt==1.5.0  # Specify a version known to work
CMD ["python", "/publisher.py"]
