from py2neo import Graph, Node, Relationship, NodeMatcher
import csv
import json

# 配置信息
NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "wlx204617")
CSV_PATH = "../data/personality_rel.csv"


# ========== 用户体系创建逻辑 ==========

# ========== 健康建议体系构建（新增逻辑）==========
def build_health_advice_system():
    """基于ID节点构建健康建议体系（核心逻辑优化）"""
    # 精确匹配ID节点
    id_node = matcher.match("Data", name="id", value=TEST_DATA["id"]).first()
    if not id_node:
        print(f"[ERROR] 未找到ID={TEST_DATA['id']}的节点，终止构建")
        return

    node_cache = {"id": id_node}
    tx = graph.begin()

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            head, rel_type, tail = row['head'], row['relation'], row['tail']

            for node_name in [head, tail]:
                if node_name not in node_cache:
                    # 先获取属性值
                    node_value = TEST_DATA.get(node_name)

                    # 处理嵌套数据结构
                    if isinstance(node_value, (dict, list)):
                        node_value = json.dumps(node_value, ensure_ascii=False)
                        data_type = "json"
                    else:
                        data_type = type(node_value).__name__ if node_value is not None else "null"

                    # 查询节点（指定标签）
                    label = "AdviceCategory" if node_name in ["health_advice", "special_management"] else "AdviceDetail"
                    existing_node = matcher.match(label, name=node_name).first()

                    if existing_node:
                        # 更新现有节点属性
                        existing_node.update({
                            "value": node_value,
                            "data_type": data_type
                        })
                        tx.push(existing_node)
                        node_cache[node_name] = existing_node
                        print(f"更新节点 {node_name}")
                    else:
                        # 创建新节点
                        new_node = Node(
                            label,
                            name=node_name,
                            value=node_value,
                            data_type=data_type
                        )
                        tx.create(new_node)
                        node_cache[node_name] = new_node
                        print(f"创建新节点 {node_name}")

            # 创建关系
            if head in node_cache and tail in node_cache:
                rel = Relationship(node_cache[head], rel_type.upper(), node_cache[tail])
                tx.create(rel)
            else:
                print(f"[WARNING] 无法创建关系 {head}->{tail}，节点缺失")

    graph.commit(tx)
    print("健康建议知识图谱构建完成！")


# ========== 测试数据 ==========
TEST_DATA = {
    "id": 1,

    # 风险评估
    "hypertension_risk": "low",
    "hypertension_prob": 0.2288,
    "cardio_risk": "medium",
    "cardio_prob": 0.3751,
    "diabetes_risk": "low",
    "diabetes_score": 4.048e-05,

    # 健康建议（直接映射CSV节点）
    "diet_recommendations": "低盐低脂饮食，每日钠摄入<5g",
    "exercise_recommendations": "每周150分钟中等强度有氧运动",
    "lifestyle_recommendations": "戒烟限酒，保持情绪稳定",
    "sleep_tips": "保证7-8小时睡眠，避免夜间电子设备使用",

    # 特殊管理（嵌套数据处理）
    "diet_tips": {"早餐": "全谷物+优质蛋白", "晚餐": "清淡易消化"},
    "herbal_tea_suggestions": ["菊花茶", "枸杞茶", "决明子茶"],
    "weekly_diet_plan": {"Day1": {"breakfast": "燕麦粥+坚果"},
        "Day2": {"breakfast": "全麦面包+鸡蛋"}},
    "weekly_exercise_plan": {"Day1": {"swim": "1小时"},
        "Day2": {"running": "2000km"}}
}

if __name__ == '__main__':
    # 初始化数据库连接
    graph = Graph(NEO4J_URI, auth=NEO4J_AUTH)
    # graph.delete_all()  # 测试时清空数据库
    matcher = NodeMatcher(graph)


    # 构建健康建议体系
    build_health_advice_system()