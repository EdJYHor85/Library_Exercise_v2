# This is where we start and existing image
FROM python:3.14-slim
# sets up the working directory inside the image created
WORKDIR /app
# copys the requirements
COPY requirements.txt .

RUN pip install -no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "02 main/cleaning_module_v2.py "]


