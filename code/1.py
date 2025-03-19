#1. 对连续变量进行标准化
#将连续变量（如血压、BMI、体重等）标准化，以消除量级的影响。
from sklearn.preprocessing import StandardScaler

# 对数值型列进行标准化
numeric_cols = data_encoded.select_dtypes(include=['float64', 'int64']).columns
scaler = StandardScaler()
data_encoded[numeric_cols] = scaler.fit_transform(data_encoded[numeric_cols])