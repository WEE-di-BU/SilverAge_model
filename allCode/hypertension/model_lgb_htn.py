import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, roc_auc_score, f1_score, precision_score, recall_score, confusion_matrix
from imblearn.over_sampling import ADASYN
import lightgbm as lgb
import joblib


# -------------------- 数据预处理模块 --------------------
def load_and_preprocess_data(file_path, target_column="hypertension", test_size=0.2, random_state=42):
    """加载并预处理数据"""
    # 加载数据
    data = pd.read_csv(file_path)

    # 确保目标列存在
    if target_column not in data.columns:
        raise ValueError(f"目标列 '{target_column}' 不在数据中")

    # 移除不希望使用的列
    columns_to_remove = ['blood_pressure_systolic', 'blood_pressure_diastolic', 'new_htn']
    # columns_to_remove = ['blood_pressure_systolic', 'blood_pressure_diastolic', 'hypertension']
    data = data.drop(columns_to_remove, axis=1, errors='ignore')

    # 对数值特征进行分箱处理
    numerical_features = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    for feature in numerical_features:
        if feature != target_column:
            data[feature + '_bin'] = pd.qcut(data[feature], q=5, duplicates='drop')

    # 对分类特征进行目标编码
    categorical_features = data.select_dtypes(include=['object', 'category']).columns.tolist()
    for feature in categorical_features:
        if feature != target_column:
            mean_encoding = data.groupby(feature)[target_column].mean()
            data[feature + '_mean_encoded'] = data[feature].map(mean_encoding)

    # 区分特征和目标
    X = data.drop(target_column, axis=1)
    y = data[target_column]

    # 区分数值型和分类型列
    numerical_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()

    # 处理缺失值
    X[numerical_features] = X[numerical_features].fillna(X[numerical_features].median())
    for col in categorical_features:
        X[col].fillna(X[col].mode()[0], inplace=True)

    # 预处理管道
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])

    X_processed = preprocessor.fit_transform(X)

    # 划分数据集
    X_train, X_test, y_train, y_test = train_test_split(
        X_processed, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y)

    return X_train, X_test, y_train, y_test, preprocessor, X.columns.tolist()


# -------------------- 回调模块 --------------------
class LightGBMMetricsCallback:
    """自定义回调函数，用于实时监控训练指标"""
    def __init__(self, X_val, y_val, metric_names=None, interval=10):
        if metric_names is None:
            metric_names = ['accuracy', 'auc', 'f1']
        self.X_val = X_val
        self.y_val = y_val
        self.metric_names = metric_names
        self.interval = interval
        self._best_score = -np.inf
        self._current_iter = 0

    def _calc_metrics(self, y_true, y_pred):
        """计算指定指标"""
        metrics = {}
        y_pred_class = (y_pred > 0.5).astype(int)

        if 'accuracy' in self.metric_names:
            metrics['accuracy'] = accuracy_score(y_true, y_pred_class)
        if 'auc' in self.metric_names:
            metrics['auc'] = roc_auc_score(y_true, y_pred)
        if 'f1' in self.metric_names:
            metrics['f1'] = f1_score(y_true, y_pred_class)
        if 'precision' in self.metric_names:
            metrics['precision'] = precision_score(y_true, y_pred_class, zero_division=0)
        if 'recall' in self.metric_names:
            metrics['recall'] = recall_score(y_true, y_pred_class)

        return metrics

    def __call__(self, env):
        """回调函数主体"""
        # 每interval轮次打印一次
        if env.iteration % self.interval != 0:
            return

        # 获取预测概率
        y_pred = env.model.predict(self.X_val)

        # 计算指标
        val_metrics = self._calc_metrics(self.y_val, y_pred)

        # 记录最佳AUC
        current_auc = val_metrics.get('auc', 0)
        if current_auc > self._best_score:
            self._best_score = current_auc
            improvement = '↑'
        else:
            improvement = '-'

        # 格式化输出
        metric_str = ' - '.join([f"{k}:{v:.4f}" for k, v in val_metrics.items()])
        print(f"Iter {env.iteration:4d} | {metric_str} | Best AUC: {self._best_score:.4f}{improvement}")


# -------------------- 模型训练模块 --------------------
def train_lightgbm(X_train, y_train, X_val=None, y_val=None, random_state=42):
    """训练LightGBM模型"""
    # 数据划分
    if X_val is None:
        X_train, X_val, y_train, y_val = train_test_split(
            X_train, y_train,
            test_size=0.3,
            stratify=y_train,
            random_state=random_state
        )

    value_counts = y_train.value_counts()
    print("类别分布:\n", value_counts)
    try:
        adasyn = ADASYN(sampling_strategy="minority", random_state=42)
        X_train, y_train = adasyn.fit_resample(X_train, y_train)
        print("过采样后类别分布:\n", y_train.value_counts())
    except ValueError as e:
        print(e)
        print("无需进行过采样，已进入下一步。")

    # 创建Dataset
    train_data = lgb.Dataset(X_train, label=y_train)
    valid_data = lgb.Dataset(X_val, label=y_val, reference=train_data)

    # 定义参数
    params = {
        'objective': 'binary',
        'metric': 'None',  # 禁用内置指标计算
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1,  # 关闭默认输出
        'random_state': random_state
    }

    # 创建回调
    metrics_callback = LightGBMMetricsCallback(
        X_val=X_val,
        y_val=y_val,
        metric_names=['accuracy', 'auc', 'f1', 'precision', 'recall'],
        interval=10
    )

    # 训练模型
    model = lgb.train(
        params,
        train_data,
        valid_sets=[valid_data],
        callbacks=[metrics_callback],
        num_boost_round=1000
    )

    return model


# -------------------- 评估模块 --------------------
def evaluate_model(model, X_test, y_test):
    """评估模型性能"""
    y_pred_prob = model.predict(X_test)
    y_pred = (y_pred_prob > 0.5).astype(int)

    print("\n最终评估结果:")
    print(f"测试集准确率: {accuracy_score(y_test, y_pred):.4f}")
    print(f"测试集AUC: {roc_auc_score(y_test, y_pred_prob):.4f}")
    print(f"测试集F1分数: {f1_score(y_test, y_pred):.4f}")
    print(f"测试集精确率: {precision_score(y_test, y_pred):.4f}")
    print(f"测试集召回率: {recall_score(y_test, y_pred):.4f}")

    # 混淆矩阵
    cm = confusion_matrix(y_test, y_pred)
    print("\n混淆矩阵:")
    print(cm)
    


# -------------------- 预测模块 --------------------
def predict_new_data(model, preprocessor, new_data_file, required_columns, target_column, encoding='utf-8', output_csv='predictions.csv'):
    """预测新数据"""
    try:
        new_data = pd.read_csv(new_data_file, encoding=encoding)
    except UnicodeDecodeError:
        try:
            new_data = pd.read_csv(new_data_file, encoding='gbk')
        except UnicodeDecodeError as u:
            print(u)
            print("文件格式有误。")
            return

    # 移除不希望使用的列
    columns_to_remove = ['blood_pressure_systolic', 'blood_pressure_diastolic']
    new_data = new_data.drop(columns_to_remove, axis=1, errors='ignore')

    # 对数值特征进行分箱处理
    numerical_features = new_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    for feature in numerical_features:
        if feature != target_column:
            new_data[feature + '_bin'] = pd.qcut(new_data[feature], q=5, duplicates='drop')
    # 对分类特征进行目标编码
    categorical_features = new_data.select_dtypes(include=['object', 'category']).columns.tolist()
    for feature in categorical_features:
        if feature != target_column:
            mean_encoding = new_data.groupby(feature)[target_column].mean()
            new_data[feature + '_mean_encoded'] = new_data[feature].map(mean_encoding)

    # 处理缺失列
    missing_columns = [col for col in required_columns if col not in new_data.columns]
    if missing_columns:
        print(f"正在处理缺失列：{missing_columns}")
        numeric_keywords = ['age', 'diabetes', 'cholesterol_level', 'obesity', 'waist_circumference', 'family_history',  'sleepHours', 'blood_pressure_systolic', 'blood_pressure_diastolic', 'fasting_blood_sugar', 'cholesterol_hdl', 'cholesterol_ldl', 'triglycerides', 'fasting_blood_sugar', 'previous_heart_disease', 'medication_usage', 'participated_in_free_screening', 'heart_attack']
        for col in missing_columns:
            if any(keyword in col for keyword in numeric_keywords):
                new_data[col] = -1
            else:
                new_data[col] = ' '

    # 只保留需要的列
    new_data = new_data[required_columns]

    # 处理缺失值
    numerical_features = new_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = new_data.select_dtypes(include=['object', 'category']).columns.tolist()

    if len(numerical_features) > 0:
        new_data[numerical_features] = new_data[numerical_features].fillna(new_data[numerical_features].median())
    if len(categorical_features) > 0:
        for col in categorical_features:
            new_data[col].fillna(new_data[col].mode()[0], inplace=True)

    # 预处理新数据
    new_data_processed = preprocessor.transform(new_data)

    # 进行预测
    predictions = model.predict(new_data_processed)

    # 创建结果数据框
    results = pd.DataFrame({
        'Patient ID': range(1, len(predictions) + 1),
        'Hypertension Probability': predictions
    })

    # 保存到CSV文件
    results.to_csv(output_csv, index=False)
    print(f"预测结果已保存到 {output_csv}")

    # 输出结果
    for i, prob in enumerate(predictions):
        print(f"患者 {i + 1} 的高血压概率: {prob:.4f}")
    return predictions


# -------------------- 主程序 --------------------
if __name__ == "__main__":
    dataset_directory = "datas/"
    target_column = "hypertension"
    # target_column = "new_htn"

    # 1. 数据预处理
    X_train, X_test, y_train, y_test, preprocessor, column_names = load_and_preprocess_data(
        dataset_directory + "heart_attack_prediction_indonesia.csv", target_column=target_column)

    # 2. 训练LightGBM模型
    print("开始训练模型...")
    model = train_lightgbm(X_train, y_train)

    # 3. 评估模型
    evaluate_model(model, X_test, y_test)

    # 4. 保存模型
    model_path = "save_model/lightgbm_model.pkl"
    joblib.dump(model, model_path)
    print(f"\n模型已保存至: {model_path}")

    # 5. 预测新数据
    print("\n开始预测新数据...")
    predict_new_data(model, preprocessor, dataset_directory + "yuce_data.csv", column_names, "hypertension")