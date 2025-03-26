import pandas as pd
import numpy as np
from joblib import load

# 加载模型
model = load('logistic_regression_model.joblib')

# 数据预处理函数
def preprocess_data(new_data):
    """
    对输入数据进行预处理，与训练时完全一致
    """
    # 1.1 基础数据处理
    df = new_data.copy()

    # 1.2 转换年龄（天→年）
    df['age'] = df['age'] / 365.25

    # 1.3 重命名列
    column_mapping = {
        'ap_hi': 'systolic_b_pressure',
        'ap_lo': 'diastolic_b_pressure',
        'gluc': 'glucose',
        'alco': 'alcohol',
        'active': 'physically_active',
        'cardio': 'cardio_disease'
    }
    df = df.rename(columns=column_mapping)

    # 1.4 数据清洗
    cleaning_rules = [
        ('height', (100, 200)),
        ('weight', (40, 200)),
        ('systolic_b_pressure', (90, 250)),
        ('diastolic_b_pressure', (60, 150)),
        ('cholesterol', [1, 2, 3]),
        ('glucose', [1, 2, 3]),
        ('gender', [1, 2])
    ]

    for col, rule in cleaning_rules:
        if isinstance(rule, list):
            df = df[df[col].isin(rule)]
        else:
            low, high = rule
            df = df[(df[col] >= low) & (df[col] <= high)]

    df = df.dropna()  # 删除缺失值

    # 1.5 创建新特征
    # BMI
    df['bmi'] = df['weight'] / (df['height'] / 100) ** 2

    # 血压分类（使用训练时的categories）
    bp_categories = ['normal', 'prehypertension', 'hypertension']
    df['blood_pressure_category'] = pd.cut(
        df['systolic_b_pressure'],
        bins=[0, 120, 140, float('inf')],
        labels=bp_categories,
        ordered=False
    )

    # 年龄分组（使用训练时的bins）
    age_bins = [30, 45, 60, 80]
    df['age_group'] = pd.cut(
        df['age'],
        bins=age_bins,
        labels=['young', 'middle_aged', 'elderly'],
        right=False,
        ordered=False
    )

    # 其他交互特征（保留与模型相关的特征）
    df['cholesterol_bmi_interaction'] = df['cholesterol'] * df['bmi']
    df['active_with_disease'] = ((df['physically_active'] == 1) & (df['cardio_disease'] == 1)).astype(int)

    # 1.6 独热编码（保留训练时的列顺序）
    categorical_cols = ['blood_pressure_category', 'age_group']
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # 1.7 删除冗余特征（与训练时一致）
    features_to_drop = [
        'id', 'gender', 'smoke', 'alcohol', 'physically_active',
        'weight', 'cholesterol', 'pressure_ratio', 'height_weight_ratio'
    ]
    df = df.drop(columns=features_to_drop, errors='ignore')

    # 1.8 标准化（使用训练时的均值和标准差）
    # 注意：这里需要使用训练集的scaler，由于之前未保存，此处重新实现标准化
    numeric_cols = [
        'age', 'height', 'systolic_b_pressure', 'diastolic_b_pressure',
        'glucose', 'bmi', 'cholesterol_bmi_interaction', 'active_with_disease'
    ]

    # 假设训练集的均值和标准差如下（实际应从训练数据获取，此处为示例）
    scaler_params = {
        'mean': np.array([53.12, 167.6, 128.4, 81.2, 1.2, 28.5, 78.2, 0.15]),
        'scale': np.array([9.8, 9.2, 15.6, 10.1, 0.45, 4.2, 22.5, 0.36])
    }

    for i, col in enumerate(numeric_cols):
        df[col] = (df[col] - scaler_params['mean'][i]) / scaler_params['scale'][i]

    return df

# 预测函数
def predict_cardio_disease(input_data):
    """
    输入：DataFrame或CSV文件路径
    输出：预测结果（0/1）和患病概率
    """
    # 处理输入数据
    if isinstance(input_data, str):  # 如果是文件路径
        new_data = pd.read_csv(input_data, sep=';')
    else:  # 假设是DataFrame
        new_data = input_data.copy()

    # 提取id列（如果存在）
    ids = new_data.get('id', [None] * len(new_data))

    # 预处理
    processed_data = preprocess_data(new_data)

    # 确保特征顺序与训练时一致
    expected_features = [
        'age', 'height', 'systolic_b_pressure', 'diastolic_b_pressure',
        'glucose', 'bmi', 'cholesterol_bmi_interaction', 'active_with_disease',
        'blood_pressure_category_prehypertension', 'blood_pressure_category_hypertension',
        'age_group_middle_aged', 'age_group_elderly'
    ]

    # 检查特征完整性
    missing_features = [f for f in expected_features if f not in processed_data.columns]
    if missing_features:
        raise ValueError(f"缺少必要特征: {missing_features}")

    processed_data = processed_data[expected_features]

    # 进行预测
    y_pred = model.predict(processed_data)
    y_pred_proba = model.predict_proba(processed_data)
    disease_probability = y_pred_proba[:, 1]

    return ids, y_pred, disease_probability