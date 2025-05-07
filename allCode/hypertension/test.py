import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import joblib

# 加载已保存的模型和预处理管道
model = joblib.load("../model/lightgbm_model.pkl")
preprocessor = joblib.load("model/preprocessor.pkl")  # 假设预处理管道已保存

# 示例数据
sample_data = {
    'age': [45],
    'diabetes': [1],
    'cholesterol_level': [240],
    'obesity': [28.5],
    'waist_circumference': [95],
    'family_history': [1],
    'sleepHours': [6.5],
    'fasting_blood_sugar': [120],
    'cholesterol_hdl': [40],
    'cholesterol_ldl': [160],
    'triglycerides': [200],
    'previous_heart_disease': [0],
    'medication_usage': [1],
    'participated_in_free_screening': [1],
    'heart_attack': [0],
    'gender': ["Male"],
    'smoking': ["Ex-smoker"]
}
df_sample = pd.DataFrame(sample_data)

# 确保列顺序与训练数据一致（此处需替换为实际训练的列名列表）
required_columns = [
    'age', 'diabetes', 'cholesterol_level', 'obesity',
    'waist_circumference', 'family_history', 'sleepHours',
    'fasting_blood_sugar', 'cholesterol_hdl', 'cholesterol_ldl',
    'triglycerides', 'previous_heart_disease', 'medication_usage',
    'participated_in_free_screening', 'heart_attack', 'gender', 'smoking'
]


# 预测函数（模拟predict_new_data的核心逻辑）
def quick_predict(model, preprocessor, data, required_columns):
    # 确保列顺序和缺失列处理
    data = data.reindex(columns=required_columns, fill_value=-1)

    # 预处理（假设与训练一致）
    processed_data = preprocessor.transform(data)

    # 预测
    proba = model.predict(processed_data)
    return proba


# 执行预测
probabilities = quick_predict(model, preprocessor, df_sample, required_columns)
print(f"预测概率: {probabilities[0]:.4f}")