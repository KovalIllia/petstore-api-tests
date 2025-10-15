FROM python:3.9-slim

WORKDIR /app

COPY . /app/

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pytest allure-python-commons pytest-html pytest-xdist

RUN mkdir -p /output/test_result

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["pytest", "-s", "--alluredir=/output/test_result"]
