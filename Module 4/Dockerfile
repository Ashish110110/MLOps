FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app

COPY [ "Pipfile", "Pipfile.lock", "./" ]

RUN pipenv install --system --deploy

COPY [ "starter.py", "./" ]

RUN mkdir -p /app/output

ENTRYPOINT ["python", "starter.py"]




# docker build -t mean-predicted-mlops-week-four:v5 .

# docker run -it --rm mean-predicted-mlops-week-four:v5 2021 4



