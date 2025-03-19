from flask import Flask, request, jsonify
from base_iris_lab1 import load_local, build, train, score, new_model

app = Flask(__name__)

# Global lists to store dataset and model indices
datasets = []
models = []

# Upload training data
@app.route('/iris/datasets', methods=['POST'])
def upload_dataset():
    """
    Upload a dataset via a CSV file.
    """
    if 'train' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['train']
    file.save('temp.csv')
    dataset_id = load_local('temp.csv')
    datasets.append(dataset_id)
    return jsonify({'dataset_id': dataset_id}), 201

# Build and train a new model
@app.route('/iris/model', methods=['POST'])
def create_model():
    """
    Create and train a new model using the specified dataset.
    """
    dataset_id = int(request.form.get('dataset'))
    model_id = new_model(dataset_id)
    models.append(model_id)
    return jsonify({'model_id': model_id}), 201

# Retrain an existing model
@app.route('/iris/model/<int:model_id>', methods=['PUT'])
def retrain_model(model_id):
    """
    Retrain an existing model using the specified dataset.
    """
    dataset_id = int(request.args.get('dataset'))
    history = train(model_id, dataset_id)
    return jsonify(history), 200

# Score a model with provided features
@app.route('/iris/model/<int:model_id>/score', methods=['GET'])
def score_model(model_id):
    """
    Score a model using the provided features.
    """
    fields = list(map(float, request.args.get('fields').split(',')))
    prediction = score(model_id, fields)
    return jsonify({'species': prediction}), 200

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)