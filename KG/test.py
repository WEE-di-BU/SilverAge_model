
from networkx import Graph

from KG.kg_node import create_neo4j_nodes

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "wlx204617")
graph = Graph(NEO4J_URI, auth=NEO4J_AUTH)
data = {
    # 核心标识
    "id": 5,

    # 基础信息（直接对应CSV的tail节点）
    "age": 34,
    "gender": "Female",
    "region": "Rural",
    "income_level": "Middle",

    # 疾病标记
    "hypertension": 0,
    "diabetes": 0,
    "previous_heart_attack": 0,  # 对应csv中的heart_attack
    "new_htn": 0,

    # 生理指标（完全匹配CSV的depends节点）
    "cholesterol_level": 227,
    "obesity": 1,
    "waist_circumference": 99,
    "height": 168,
    "weight": 62,
    "blood_pressure_systolic": 106,
    "blood_pressure_diastolic": 80,
    "fasting_blood_sugar": 70,
    "cholesterol_hdl": 53,
    "cholesterol_ldl": 124,
    "triglycerides": 186,
    "cholesterol": 3,
    "gluc": 3,

    # 生活习惯（名称与CSV完全一致）
    "family_history": 1,
    "smoking_status": "Past",
    "alcohol_consumption": "Moderate",
    "physical_activity": "Moderate",
    "dietary_habits": "Healthy",
    "air_pollution_exposure": "Low",
    "stress_level": "High",
    "sleep_hours": 5.2,
    "smoke": 0,
    "alco": 0,
    "active": 1,
    "HvyAlcoholConsump": 0,
    "PhysActivity": 1,
    "Fruits": 0,
    "Veggies": 0,

    # 医疗检查结果
    "EKG_results": "Abnormal",
    "medication_usage": 1,
    "participated_in_free_screening": 1,

    # 健康评估
    "GenHlth": 5,
    "MentHlth": 18,
    "PhysHlth": 15,
    "DiffWalk": 1,

    # 社会因素
    "Education": 4,
    "Income": 3,

    # 预测节点（值精确到CSV定义）
    "Hypertension_Probability": 0.2288,
    "Cardiovascular_Probability": 0.3751,
    "Diabetes_Risk_Score": 4.048e-05
}
create_neo4j_nodes(data,graph)