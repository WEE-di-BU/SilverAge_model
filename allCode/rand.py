import pandas as pd
import numpy as np


def process_probability(input_path, output_path):
    """
    处理CSV文件中的probability列：
    - 将0值替换为[0, 0.1)区间的随机数
    - 保留四位小数
    - 非零值保持不变
    """
    # 读取CSV文件
    df = pd.read_csv(input_path)

    # 检查是否存在probability列
    if 'probability' not in df.columns:
        raise ValueError("CSV文件中不存在'probability'列")

    # 定位所有零值位置
    zero_mask = df['probability'] == 0

    # 生成随机数 (范围[0, 0.1)，保留四位小数)
    random_values = np.random.uniform(0, 0.1, size=zero_mask.sum()).round(4)

    # 替换零值
    df.loc[zero_mask, 'probability'] = random_values

    # 保存处理后的数据
    df.to_csv(output_path, index=False)
    print(f"处理完成，共修改 {len(random_values)} 条零值记录")


# 使用示例
process_probability("../data/c_predict.csv", "../data/output.csv")