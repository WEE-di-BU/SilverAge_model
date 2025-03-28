from flask import Flask, request, jsonify
import pandas as pd
from xxg_predict import predict_cardio_disease
import numpy as np

app = Flask(__name__)

@app.route('/cardiovascular-predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("接收到的完整数据：", data)

        # 判断输入是单个对象还是列表
        if isinstance(data, dict):
            data = [data]
            single_input = True
        else:
            single_input = False

        df = pd.DataFrame(data)

        ids, y_pred, disease_probability = predict_cardio_disease(df)

        results = []
        for i in range(len(y_pred)):
            # 确保每个值都是 Python 原生类型
            result = {
                "id": int(ids[i]) if isinstance(ids[i], np.int64) else ids[i],
                "prediction": int(y_pred[i]),
                "probability": float(f"{disease_probability[i]:.4f}")
            }
            results.append(result)

        print(results)

        # 根据输入类型决定返回单个对象还是列表
        if single_input:
            print(results[0])
            return jsonify(results[0])
        else:
            return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)