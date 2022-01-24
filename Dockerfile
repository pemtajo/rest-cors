FROM python:3.7-alpine 

# Install dependencies.
ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# Copy code.
COPY . .

CMD python /proxy.py
