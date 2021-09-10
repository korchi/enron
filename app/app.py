import time

from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_VERSION = 'model_V0.pkl'
VECTORIZER_VERSION = 'vectorizer_V0.pkl'


# load model assets
# vectorizer_path = os.path.join(os.getcwd(), 'model_assets', VECTORIZER_VERSION)
# model_path = os.path.join(os.getcwd(), 'model_assets', MODEL_VERSION)
# vectorizer = pickle.load(open(vectorizer_path, 'rb'))
# model = pickle.load(open(model_path, 'rb'))


@app.route('/', methods=['POST'])
def predict():
    """ Main webpage with user input through form and prediction displayed
    :return: main webpage host, displays prediction if user submitted in text field
    """

    msg = request.json()
    print(msg['email'])
    return {'message': 'This is what I got',
            'input': jsonify(msg)}


@app.route('/predict', methods=['POST'])
def predict_api():
    """ endpoint for model queries (non gui)
    :return: json, model prediction and response time
    """
    start_time = time.time()

    # request_data = request.json
    # input_text = request_data['data']
    # input_text = clean_text(input_text)
    # input_text = vectorizer.transform([input_text])
    # prediction = model.predict(input_text)
    # prediction = 'Cyber-Troll' if prediction[0] == 1 else "Non Cyber-Troll"  # post processing
    #
    # response = {'prediction': prediction, 'response_time': time.time() - start_time}
    response = {'prediction': 'dummy'}
    return jsonify(response)


def load_model():
    print('loading model')


def main():
    load_model()
    app.run(host="0.0.0.0", port=5000)


if __name__ == '__main__':
    main()
