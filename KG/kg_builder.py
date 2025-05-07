from py2neo import Graph, Node, Relationship, NodeMatcher
import csv

# 配置信息
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "wlx204617")
CSV_DATA_PATH = "../data/combined_allData_reInfor.csv"
CSV_REL_PATH = "../data/concept_rel.csv"

# 初始化图数据库连接
graph = Graph(NEO4J_URI, auth=NEO4J_AUTH)
matcher = NodeMatcher(graph)


def find_all_user_data_in_csv(user_id):
    """在CSV文件中查找特定用户ID的所有数据记录"""
    user_data_list = []
    with open(CSV_DATA_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if int(row.get('userId', 0)) == user_id:
                # 转换数据类型
                processed_data = {}
                for key, value in row.items():
                    if value.isdigit():
                        processed_data[key] = int(value)
                    elif is_float(value):
                        processed_data[key] = float(value)
                    elif value.lower() in ['true', 'false']:
                        processed_data[key] = value.lower() == 'true'
                    else:
                        processed_data[key] = value
                user_data_list.append(processed_data)
    return user_data_list


def is_float(value):
    """检查字符串是否可以转换为浮点数"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_or_create_user(user_data):
    """动态创建/获取用户节点"""
    existing_user = matcher.match("User", userId=user_data["userId"]).first()
    if existing_user:
        print(f"用户 {user_data['userId']} 已存在，直接使用")
        return existing_user

    new_user = Node("User",
                    name=user_data["username"],
                    userId=user_data["userId"],
                    username=user_data["username"],
                    role="user")
    graph.create(new_user)
    print(f"创建新用户：{user_data['userId']}")
    return new_user


def build_kg_for_user(user_id):
    """为指定用户构建知识图谱（处理多条记录）"""
    # 查找该用户的所有数据记录
    user_data_list = find_all_user_data_in_csv(user_id)
    if not user_data_list:
        return False, f"未找到用户 {user_id} 的数据"

    # 检查是否已存在该用户的任何知识图谱
    existing_user = matcher.match("User", userId=user_id).first()
    if existing_user and list(graph.match((existing_user,), "OWNS")):
        return False, f"用户 {user_id} 的知识图谱已存在"

    success_count = 0
    for i, user_data in enumerate(user_data_list, 1):
        # 创建用户节点（只在第一次创建）
        if i == 1:
            admin = get_or_create_user({
                "userId": user_data["userId"],
                "username": user_data.get("username", f"user_{user_id}")
            })

        # 为每条记录创建唯一ID节点
        record_id = f"{user_id}_{i}"
        id_node = Node("Data", name="id", value=record_id, record_index=i)
        graph.create(id_node)
        graph.create(Relationship(admin, "OWNS", id_node))

        # 节点缓存（每条记录独立缓存）
        node_cache = {
            "admin": admin,
            "id": id_node,
            str(user_data["userId"]): admin
        }

        # 构建知识图谱关系
        with open(CSV_REL_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                head, relation, tail = row['head'], row['relation'], row['tail']

                for node_name in [head, tail]:
                    if node_name not in node_cache:
                        node_value = user_data.get(node_name, None)

                        if "Probability" in node_name or "Risk" in node_name:
                            label = "Prediction"
                        elif relation == 'depends':
                            label = "Factor"
                        else:
                            label = "Data"

                        # 为节点添加记录索引标记
                        new_node = Node(label, name=node_name, value=node_value, record_index=i)
                        graph.create(new_node)
                        node_cache[node_name] = new_node

                rel_type = "PREDICTS" if relation == "predict" else "DEPENDS_ON"
                graph.create(Relationship(node_cache[head], rel_type, node_cache[tail]))

        success_count += 1
        print(f"已为用户 {user_id} 创建第 {i} 条记录的知识图谱")

    return True, f"成功为用户 {user_id} 创建 {success_count} 条记录的知识图谱"