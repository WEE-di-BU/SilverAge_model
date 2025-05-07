from py2neo import Graph, Node, Relationship, NodeMatcher
import csv

# 配置信息
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "wlx204617")
CSV_PATH = "../data/concept_rel.csv"


# ========== 用户体系创建逻辑修改 ==========
def get_or_create_user(user_data):
    """动态创建/获取用户节点（核心修改点）"""
    # 检查用户是否存在
    existing_user = matcher.match("User", userId=user_data["userId"]).first()

    if existing_user:
        print(f"用户 {user_data['userId']} 已存在，直接使用")
        return existing_user

    # 创建新用户节点
    new_user = Node("User",
                    name=user_data["username"],
                    userId=user_data["userId"],
                    username=user_data["username"],
                    role="administrator")
    graph.create(new_user)
    print(f"创建新用户：{user_data['userId']}")
    return new_user


# ========== 核心数据节点创建（新增存在性检查）==========
def get_or_create_friends(admin):
    # 检查是否已存在相同值的id节点
    existing_id_node = matcher.match("Data", name="id", value=TEST_DATA["id"]).first()
    if existing_id_node:
        id_node = existing_id_node
        print(f"复用已存在的Data节点：id（值={TEST_DATA['id']}）")
    else:
        id_node = Node("Data", name="id", value=TEST_DATA["id"])
        graph.create(id_node)
        print(f"创建新Data节点：id（值={TEST_DATA['id']}）")

    graph.create(Relationship(admin, "OWNS", id_node))

    # 节点缓存（新增用户缓存）
    node_cache = {
        "admin": admin,
        "id": id_node,
        str(TEST_DATA["userId"]): admin
    }

    # 读取CSV文件构建图谱（保持原有逻辑）
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            head, relation, tail = row['head'], row['relation'], row['tail']

            # 处理头尾节点
            for node_name in [head, tail]:
                if node_name not in node_cache:
                    node_value = TEST_DATA.get(node_name, None)

                    # 标签分类逻辑保持不变
                    if "Probability" in node_name or "Risk" in node_name:
                        label = "Prediction"
                    elif relation == 'depends':
                        label = "Factor"
                    else:
                        label = "Data"

                    # 对id节点进行二次校验（防御性编程）
                    if node_name == "id" and label == "Data":
                        existing = matcher.match(label, name=node_name, value=node_value).first()
                        if existing:
                            print(f"CSV中发现已存在的Data节点：{node_name}（值={node_value}）")
                            new_node = existing
                        else:
                            new_node = Node(label, name=node_name, value=node_value)
                            graph.create(new_node)
                    else:
                        new_node = Node(label, name=node_name, value=node_value)
                        graph.create(new_node)

                    node_cache[node_name] = new_node

            # 创建关系
            rel_type = "PREDICTS" if relation == "predict" else "DEPENDS_ON"
            graph.create(Relationship(node_cache[head], rel_type, node_cache[tail]))

    print("知识图谱构建完成！")




if __name__ == '__main__':
    TEST_DATA = {
        # 核心标识
        "userId": 1001,  # 新增用户唯一标识 [3,7](@ref)
        "username": "u1",  # 新增用户名
        "id": 1,

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

    # 连接数据库
    graph = Graph(NEO4J_URI, auth=NEO4J_AUTH)
    graph.delete_all()  # 测试时清空数据库
    matcher = NodeMatcher(graph)

    # 创建/获取用户节点
    admin = get_or_create_user({
        "userId": TEST_DATA["userId"],
        "username": TEST_DATA["username"]
    })

    get_or_create_friends(admin)