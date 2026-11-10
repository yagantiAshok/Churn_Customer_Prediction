FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN sed -i 's/\r$//' start.sh
RUN chmod +x start.sh

EXPOSE 8000
EXPOSE 8501

CMD ["/bin/bash", "/app/start.sh"]