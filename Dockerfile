FROM python
COPY . /app/
WORKDIR /app/
RUN cd /app/
RUN pip install -r /app/requirements.txt
CMD ["python", "main.py"]