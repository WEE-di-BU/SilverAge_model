from .Q_Female import type2_female_raw_a, type2_female_raw_b, type2_female_raw_c
from .Q_Male import type2_male_raw_a, type2_male_raw_b, type2_male_raw_c

def calculate_risk_score(data):
    # 提取用户输入的数据
    age = data['age']
    gender = data['gender']
    ethrisk = data['ethrisk']
    smoke_cat = data['smoke_cat']
    fh_diab = data.get('fh_diab', 0)
    b_cvd = data.get('b_cvd', 0)
    b_treatedhyp = data.get('b_treatedhyp', 0)
    b_learning = data.get('b_learning', 0)
    b_manicschiz = data.get('b_manicschiz', 0)
    b_corticosteroids = data.get('b_corticosteroids', 0)
    b_statin = data.get('b_statin', 0)
    b_atypicalantipsy = data.get('b_atypicalantipsy', 0)
    height = data['height']  # 身高（厘米）
    weight = data['weight']  # 体重（千克）
    town = data.get('town', 0.5)  # 默认值为0.5
    fbs = data.get('fbs', None)
    hba1c = data.get('hba1c', None)

    #BMI
    height_m = height / 100
    bmi = weight / (height_m ** 2)

    # 根据性别选择模型
    if gender == 1:  # 男性
        if fbs is not None and hba1c is not None:
            #C
            score = type2_male_raw_c(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, hba1c, smoke_cat, 10, town)
        elif fbs is not None:
            #B
            score = type2_male_raw_b(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fbs, fh_diab, smoke_cat, 10, town)
        elif hba1c is not None:
            #C
            score = type2_male_raw_c(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, hba1c, smoke_cat, 10, town)
        else:
            #A
            score = type2_male_raw_a(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, smoke_cat, 10, town)
    elif gender == 2:  # 女性
        if fbs is not None and hba1c is not None:
            #C
            score = type2_female_raw_c(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, hba1c, smoke_cat, 10, town)
        elif fbs is not None:
            #B
            score = type2_female_raw_b(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fbs, fh_diab, smoke_cat, 10, town)
        elif hba1c is not None:
            #C
            score = type2_female_raw_c(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, hba1c, smoke_cat, 10, town)
        else:
            #A
            score = type2_female_raw_a(age, b_atypicalantipsy, b_corticosteroids, b_cvd, b_learning, b_manicschiz, b_statin, b_treatedhyp, bmi, ethrisk, fh_diab, smoke_cat, 10, town)
    else:
        raise ValueError("无效的性别输入！")

    return score

# 示例调用
if __name__ == "__main__":
    #示例
    user_data = {
        "age": 64,
        "gender": 1,  # 1 代表男性，2 代表女性
        "ethrisk": 1,  # 种族分类
        "smoke_cat": 3,  # 吸烟分类
        "fh_diab": 1,  # 直系亲属是否患有糖尿病
        "b_cvd": 0,  # 是否曾患过心脏病、心绞痛、卒中或 TIA
        "b_treatedhyp": 0,  # 是否患有需要治疗的高血压
        "b_learning": 0,  # 是否有学习障碍
        "b_manicschiz": 0,  # 是否有躁狂抑郁症或精神分裂症
        "b_corticosteroids": 0,  # 是否正在服用普通的类固醇片剂
        "b_statin": 0,  # 是否在服用他汀类药物
        "b_atypicalantipsy": 0,  # 是否服用非典型抗精神病药物
        "height": 175,  # 身高（厘米）
        "weight": 75,  # 体重（千克）
        "town": 0.6,  # 城镇变量
        #"hba1c": 6.5  # 糖化血红蛋白
        #"fbs": 6.0  # 空腹血糖（mmol/L）
    
    }

    try:
        score = calculate_risk_score(user_data)
        print(f"您的2型糖尿病风险评分为: {score:.2f}%")
    except ValueError as e:
        print(e)