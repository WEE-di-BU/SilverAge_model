from py2neo import Graph, Node, Relationship, NodeMatcher
import csv

# 配置信息
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "wlx204617")
CSV_DATA_PATH = "../data/combined_allData_reInfor.csv"  # 假设这是包含用户数据的CSV文件
CSV_REL_PATH = "../data/concept_rel.csv"  # 这是原来的关系定义文件


# ========== 用户体系创建逻辑修改 ==========
def get_or_create_user(user_data):
    """动态创建/获取用户节点"""
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


# ========== 核心数据节点创建 ==========
def get_or_create_friends(admin, user_data):
    # 检查是否已存在相同值的id节点
    existing_id_node = matcher.match("Data", name="id", value=user_data["id"]).first()
    if existing_id_node:
        id_node = existing_id_node
        print(f"复用已存在的Data节点：id（值={user_data['id']}）")
    else:
        id_node = Node("Data", name="id", value=user_data["id"])
        graph.create(id_node)
        print(f"创建新Data节点：id（值={user_data['id']}）")

    graph.create(Relationship(admin, "OWNS", id_node))

    # 节点缓存（新增用户缓存）
    node_cache = {
        "admin": admin,
        "id": id_node,
        str(user_data["userId"]): admin
    }

    # 读取关系CSV文件构建图谱
    with open(CSV_REL_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            head, relation, tail = row['head'], row['relation'], row['tail']

            # 处理头尾节点
            for node_name in [head, tail]:
                if node_name not in node_cache:
                    node_value = user_data.get(node_name, None)

                    # 标签分类逻辑保持不变
                    if "Probability" in node_name or "Risk" in node_name:
                        label = "Prediction"
                    elif relation == 'depends':
                        label = "Factor"
                    else:
                        label = "Data"

                    # 对id节点进行二次校验
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

    print(f"用户 {user_data['userId']} 的知识图谱构建完成！")


def read_user_data_from_csv(csv_path):
    """从CSV文件中读取用户数据"""
    user_data_list = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 转换数据类型
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif is_float(value):
                    row[key] = float(value)
                elif value.lower() in ['true', 'false']:
                    row[key] = value.lower() == 'true'
            user_data_list.append(row)
    return user_data_list


def is_float(value):
    """检查字符串是否可以转换为浮点数"""
    try:
        float(value)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    # 配置参数
    MAX_RECORDS = 10  # 可以修改这个数字控制读取的记录数

    # 连接数据库
    graph = Graph(NEO4J_URI, auth=NEO4J_AUTH)
    graph.delete_all()  # 测试时清空数据库
    matcher = NodeMatcher(graph)

    # 从CSV读取用户数据
    user_data_list = read_user_data_from_csv(CSV_DATA_PATH)

    # 只取指定数量的数据
    selected_users = user_data_list[:MAX_RECORDS]
    print(f"将从CSV文件中读取前{len(selected_users)}条数据构建知识图谱...")

    # 处理选定的用户数据
    for user_data in selected_users:
        # 创建/获取用户节点
        admin = get_or_create_user({
            "userId": user_data["userId"],
            "username": user_data["username"]
        })

        get_or_create_friends(admin, user_data)

    print(f"已完成前{len(selected_users)}条数据的知识图谱构建！")