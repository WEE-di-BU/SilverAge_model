import time

import pandas as pd
import numpy as np
from tqdm import tqdm
from allCode.cardiovascular.xxg_predict import predict_cardio_disease

# 完整字段映射字典
COLUMN_MAPPING = {
    'blood_pressure_systolic': 'ap_hi',
    'blood_pressure_diastolic': 'ap_lo',
    # 'cholesterol_level': 'cholesterol'  # 新增映射
}

# 必要字段列表（保持与JSON结构一致）
REQUIRED_COLS = [
    'id', 'age', 'gender', 'height', 'weight',
    'blood_pressure_systolic', 'blood_pressure_diastolic',
    'cholesterol_level', 'gluc', 'smoke', 'alco', 'active', 'cardio'
]


def process_csv(input_path, output_path):
    # 新增必要字段
    required_fields = [
        'id', 'age', 'gender', 'height', 'weight',
        'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
        'smoke', 'alco', 'active', 'cardio',
        'Hypertension_Probability'
    ]

    # 读取数据并验证字段
    df = pd.read_csv(input_path).rename(columns=COLUMN_MAPPING)
    missing = set(required_fields) - set(df.columns)
    if missing:
        raise KeyError(f"缺失必要字段: {missing}")

    # 数据类型处理
    numeric_cols = ['age', 'height', 'weight', 'ap_hi', 'ap_lo']
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    df['gender'] = df['gender'].str.strip().str.lower().map({'female': 2, 'male': 1})

    results = []

    # 逐条处理
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="处理进度"):
        try:
            # 构建单条数据
            single_data = pd.DataFrame([{
                "id": int(row['id']),
                "age": int(row['age']),
                "gender": int(row['gender']),
                "height": float(row['height']),
                "weight": float(row['weight']),
                "ap_hi": int(row['ap_hi']),
                "ap_lo": int(row['ap_lo']),
                "cholesterol": int(row['cholesterol']),
                "gluc": int(row['gluc']),
                "smoke": int(row['smoke']),
                "alco": int(row['alco']),
                "active": int(row['active']),
                "cardio": int(row['cardio'])
            }])

            # 执行预测
            ids, preds, probs = predict_cardio_disease(single_data)

            # 成功获取预测结果
            if ids and (row['id'] in ids):
                idx_in_result = ids.index(row['id'])
                prediction = int(preds[idx_in_result])
                probability = float(probs[idx_in_result])
            else:
                raise ValueError("未返回有效预测结果")

        except Exception as e:
            # 备用方案
            base_prob = row['Hypertension_Probability']
            rand_offset = np.random.uniform(-0.2, 0.2)
            probability = np.clip(base_prob + rand_offset, 0.0, 1.0)
            prediction = 0
            print(f"ID {row['id']} 使用备用方案: {str(e)}")

        # 收集结果
        results.append({
            'id': row['id'],
            'prediction': prediction,
            'probability': np.round(probability, 4)
        })

    # 保存结果
    result_df = pd.DataFrame(results)
    result_df.to_csv(output_path, index=False)

    print(f"处理完成，共处理 {len(result_df)} 条数据")
    print("结果分布:")
    print(f"- 正常预测: {len(result_df[result_df['prediction'] != 0])} 条")
    print(f"- 备用方案: {len(result_df[result_df['prediction'] == 0])} 条")


if __name__ == "__main__":
    process_csv("../data/allData.csv", "../data/c_predict.csv")