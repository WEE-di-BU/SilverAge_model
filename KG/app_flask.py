from flask import Flask, request, jsonify
from flask_cors import CORS
from py2neo import Graph

from kg_builder import build_kg_for_user


app = Flask(__name__)
CORS(app)

NEO4J_URI = "bolt://localhost:7687"
NEO4J_AUTH = ("neo4j", "wlx204617")
graph = Graph(NEO4J_URI, auth=NEO4J_AUTH)

@app.route('/build_kg', methods=['POST'])
def handle_build_kg():
    data = request.get_json()
    user_id = data.get('userId')

    if not user_id:
        return jsonify({
            'success': False,
            'message': '缺少userId参数'
        }), 400

    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({
            'success': False,
            'message': 'userId必须是整数'
        }), 400

    success, message = build_kg_for_user(user_id)

    return jsonify({
        'success': success,
        'message': message
    })


@app.route('/get_kg_data/<int:user_id>', methods=['GET'])
def get_kg_data(user_id):
    try:
        # 查询用户节点及其关联的所有节点和关系
        query = """
        MATCH (user:User {userId: $user_id})-[:OWNS]->(id:Data)
        MATCH path=(id)-[r*]->(n)
        RETURN user, nodes(path) as nodes, relationships(path) as rels
        """
        result = graph.run(query, user_id=user_id).data()

        if not result:
            return jsonify({'success': False, 'message': '未找到用户图谱数据'}), 404

        # 使用字典存储节点ID映射
        node_id_map = {}
        nodes = []
        relationships = []

        for record in result:
            for node in record['nodes']:
                # 为每个节点创建唯一标识符
                if node.identity not in node_id_map:
                    node_data = dict(node)
                    node_data['id'] = f"node_{node.identity}"  # 添加前端可识别的ID
                    node_id_map[node.identity] = node_data['id']
                    nodes.append(node_data)

            for rel in record['rels']:
                relationships.append({
                    'source': node_id_map[rel.start_node.identity],
                    'target': node_id_map[rel.end_node.identity],
                    'type': type(rel).__name__
                })

        return jsonify({
            'success': True,
            'data': {
                'nodes': nodes,
                'relationships': relationships
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)