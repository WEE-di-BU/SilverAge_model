import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# 加载数据
data = pd.read_csv("Dataset.csv")

# 数据预处理
data.fillna(data.median(), inplace=True)

# 特征选择
features = [
    'HighBP', 'HighChol', 'CholCheck', 'BMI', 'Smoker', 'Stroke', 'HeartDiseaseorAttack',
    'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump', 'AnyHealthcare',
    'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk', 'Sex', 'Age',
    'Education', 'Income'
]
X = data[features]
y = data['Diabetes_012']

# 绘制特征相关性热力图
plt.figure(figsize=(14, 10))
correlation_matrix = X.corr()
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
plt.title("Feature Correlation Heatmap")
plt.show()

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 模型训练
model = LinearRegression()
model.fit(X_train, y_train)

# 模型评估
y_pred = model.predict(X_test)

# 计算评估指标
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

joblib.dump(model, 'diabetes_linear_regression_model.pkl')

# 查看模型的系数
coefficients = pd.DataFrame(model.coef_, index=features, columns=['Coefficient'])
print(coefficients)

# 绘制人群画像
# 选择一些关键特征进行可视化
key_features = [
    'BMI', 'Age', 'Sex', 'Smoker', 'HighBP', 'HighChol', 'Stroke',
    'HeartDiseaseorAttack', 'PhysActivity', 'Fruits', 'Veggies', 'HvyAlcoholConsump',
    'AnyHealthcare', 'NoDocbcCost', 'GenHlth', 'MentHlth', 'PhysHlth', 'DiffWalk',
    'Education', 'Income'
]

# 调整子图布局
n_features = len(key_features)
n_cols = 3
n_rows = (n_features + n_cols - 1) // n_cols  # 计算需要的行数

# 增大画布大小
plt.figure(figsize=(20, 6 * n_rows))  # 每行的高度增加到6英寸
for i, feature in enumerate(key_features, 1):
    plt.subplot(n_rows, n_cols, i)
    if data[feature].dtype == 'int64' or data[feature].dtype == 'float64':
        # 数值型特征：绘制小提琴图
        sns.violinplot(x='Diabetes_012', y=feature, data=data, hue='Diabetes_012', palette='viridis', split=True, legend=False)
        plt.title(f"Distribution of {feature} by Diabetes Status", fontsize=12)
        plt.xlabel("Diabetes Status", fontsize=10)
        plt.ylabel(feature, fontsize=10)
    else:
        # 分类特征：绘制柱状图
        sns.countplot(x=feature, hue='Diabetes_012', data=data, palette='viridis')
        plt.title(f"Distribution of {feature} by Diabetes Status", fontsize=12)
        plt.xlabel(feature, fontsize=10)
        plt.ylabel("Count", fontsize=10)

    # 调整每个子图的布局
    plt.xticks(rotation=45, fontsize=8)
    plt.yticks(fontsize=8)

plt.tight_layout()
plt.show()