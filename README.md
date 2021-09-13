# enron

ML project providing REST API to predict suspicious text, e.g., suspicious emails from Enron Email Dataset.

## Build
`docker build . -t enron`

## Run
`docker run --rm -p 5000:5000 enron`

## Test
`curl -d 'Am I fraudulent? I do not think so.'  -H "Content-Type: text/html; charset=UTF-8" -X POST 192.168.1.18:5000`