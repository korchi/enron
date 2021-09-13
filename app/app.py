import datetime
import logging
import os
from configparser import ConfigParser
from textwrap import wrap

from flask import Flask, request, jsonify

from models.embedding import EmbeddingModel

app = Flask(__name__)
model = None
config = None


def load_model(cfg: ConfigParser):
    model_tmp = EmbeddingModel(cfg)
    return model_tmp


@app.route("/", methods=["POST"], defaults={"path": ""})
def predict(path):

    print("================================================================")
    print(f"*** Received data at: {path}")

    print("\n** data:")
    print("\n".join(wrap(request.data.decode('utf-8'))))
    data = request.data.decode('utf-8')
    prediction: dict = model.predict(data)

    to_return = {
        "prediction": prediction,
        "timestamp": datetime.datetime.now()
    }

    return jsonify(to_return)


def __config_reader():
    cfg = ConfigParser()
    cfg_path = os.path.join(os.getcwd(), "cfg", "config.ini")
    logging.info(f'reading config file from {cfg_path}')
    cfg.read(cfg_path)
    return cfg


def main():
    global model
    logging.basicConfig()
    logging.root.setLevel(logging.NOTSET)
    logging.info('Started')

    cfg = __config_reader()

    model = load_model(cfg)
    app.run(host=cfg["APP"]["host"], port=cfg.getboolean("APP", "port"), debug=True)
    logging.info('Finished')


if __name__ == '__main__':
    main()
