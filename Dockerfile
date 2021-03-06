FROM python:3.8-slim

WORKDIR /app
COPY . /app

#COPY models/svm.pckl /app/models/

# Install required packages
RUN pip install --no-cache-dir poetry==1.1.7
RUN poetry config virtualenvs.create false
RUN poetry install -v --no-dev --no-interaction --no-ansi
RUN poetry run python -m spacy download en_core_web_sm

# Container port on which the server will be listening
EXPOSE 5000

# Launch server app
CMD ["poetry","run","python", "app/app.py"]