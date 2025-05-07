from py2neo import Node, Relationship


def create_neo4j_nodes(data, graph):
    """核心节点创建函数"""
    try:
        # 创建Admin用户体系
        admin = Node("User", name="admin", role="administrator")
        id_node = Node("Data", name="id", value=data["id"])
        graph.create(Relationship(admin, "OWNS", id_node))

        # 创建其他节点（动态注入值）
        nodes = {}
        for key, value in data.items():
            if key not in ["id"]:  # 跳过已处理的id
                label = "Prediction" if ("Probability" in key or "Risk" in key) else "Data"
                nodes[key] = Node(label, name=key, value=value)
                graph.create(nodes[key])

        return True
    except Exception as e:
        print(f"节点创建失败: {str(e)}")
        return False