from flask import Flask, request, jsonify
import pandas as pd
from allCode.cardiovascular.xxg_predict import predict_cardio_disease
import numpy as np
from allCode.glycuresis.main import calculate_risk_score
import allCode.ai.deepseekApi as deepseekApi

app = Flask(__name__)

@app.route('/cardiovascular-predict', methods=['POST'])
def cardiovascular_predict():
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

        # 根据输入类型决定返回单个对象还是列表
        if single_input:
            return jsonify(results[0])
        else:
            return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/glycuresis-predict', methods=['POST'])
def glycuresis_predict():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        score = calculate_risk_score(data)
        score = score / 100
        formatted_score = float(f"{score:.4f}")
        return jsonify({"probability": formatted_score}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500

# @app.route('/predict/hypertension-predict', methods=['POST'])  # 修改为 POST 请求
# def predict_htn():
#     try:
#         # 获取SpringBoot发送的 JSON 数据
#         data = request.get_json()
#         if data is None:
#             return jsonify({"error": "Invalid JSON data"}), 400
#
#         print(f'predict_htn Received data: {data}')
#
#         return data
#
#     except Exception as e:
#         print(f"错误: {e}")  # 打印错误信息
#         return jsonify({'error': str(e)}), 400
#
# @app.route('/predict/report-explain', methods=['POST'])  # 修改为 POST 请求
# def report_explain():
#     try:
#         # 获取SpringBoot发送的 JSON 数据
#         data = request.get_json()
#         if data is None:
#             return jsonify({"error": "Invalid JSON data"}), 400
#
#         print(f'report-explain Received data: {data}')
#         explain_results = deepseekApi.interpret_health_report(data["contents"])
#
#         return explain_results
#
#     except Exception as e:
#         print(f"错误: {e}")  # 打印错误信息
#         return jsonify({'error': str(e)}), 400
#
#

if __name__ == '__main__':
    app.run(debug=True)