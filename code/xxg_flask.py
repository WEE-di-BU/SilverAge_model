from flask import Flask, request, jsonify
import pandas as pd
from xxg_predict import predict_cardio_disease
import numpy as np

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if isinstance(data, dict):
            data = [data]
        df = pd.DataFrame(data)

        ids, y_pred, disease_probability = predict_cardio_disease(df)

        results = []
        for i in range(len(y_pred)):
            # 确保每个值都是 Python 原生类型
            result = {
                "id": int(ids[i]) if isinstance(ids[i], np.int64) else ids[i],
                "预测类别": int(y_pred[i]),
                "患病概率": float(f"{disease_probability[i]:.4f}")
            }
            results.append(result)

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)