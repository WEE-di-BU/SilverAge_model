# 前三千条数据是，后面的3001-70001未考虑
import pandas as pd
import numpy as np
from datetime import datetime
from tqdm import tqdm


class AdvancedHealthRecommender:
    def __init__(self):
        # 定义风险等级阈值 (高血压、心脑血管、糖尿病)
        self.risk_thresholds = {
            'hypertension': {'low': 0.3, 'medium': 0.6, 'high': 1.0},
            'cardiovascular': {'low': 0.25, 'medium': 0.5, 'high': 1.0},
            'diabetes': {'low': 3.0, 'medium': 6.0, 'high': 10.0}
        }

        # 定义修正规则
        self.correction_rules = {
            'sleep_hours': (4, 12),  # 合理睡眠时长范围
            'physical_activity': ['Sedentary', 'Light', 'Moderate', 'Active'],
            'dietary_habits': ['Unhealthy', 'Average', 'Healthy'],
            'blood_pressure_systolic': (90, 200),
            'blood_pressure_diastolic': (60, 120),
            'fasting_blood_sugar': (70, 300),
            'bmi': (16, 40)  # BMI合理范围
        }

        # 扩展食物库 (增加加餐选项)
        self.food_library = {
            'breakfast': {
                'general': ['全麦面包+鸡蛋+牛奶', '燕麦粥+坚果', '杂粮煎饼+豆浆'],
                'diabetes': ['杂粮粥+水煮蛋', '无糖豆浆+全麦面包', '蔬菜沙拉+鸡胸肉'],
                'hypertension': ['低脂牛奶+香蕉', '全麦饼干+无糖酸奶', '红薯+鸡蛋'],
                'elderly': ['小米粥+蒸南瓜', '藕粉+核桃', '鸡蛋羹+杂粮馒头']
            },
            'lunch': {
                'general': ['糙米饭+清蒸鱼+炒时蔬', '荞麦面+鸡丝+凉拌菜', '红薯+清炒虾仁+西兰花'],
                'diabetes': ['杂粮饭+白灼虾+苦瓜', '魔芋丝+凉拌鸡胸肉+菠菜', '藜麦饭+蒸鱼+芦笋'],
                'hypertension': ['燕麦饭+清蒸鸡+蒜蓉西兰花', '小米饭+豆腐+炒青菜', '玉米+蒸鱼+凉拌木耳'],
                'elderly': ['软米饭+蒸鱼+南瓜', '龙须面+碎肉+胡萝卜', '芋头+豆腐羹+青菜']
            },
            'dinner': {
                'general': ['小米粥+蒸南瓜+豆腐', '杂粮馒头+炒时蔬+鸡蛋汤', '红薯粥+凉拌黄瓜+鱼肉'],
                'diabetes': ['蔬菜汤+鸡胸肉+杂粮饼', '魔芋丝+白灼虾+炒苦瓜', '杂豆粥+凉拌豆腐+青菜'],
                'hypertension': ['燕麦粥+凉拌木耳+蒸茄子', '红豆汤+全麦面包+蔬菜', '小米粥+蒸鱼+蒜蓉菠菜'],
                'elderly': ['山药粥+蒸蛋+软烂青菜', '南瓜汤+鱼肉丸+豆腐', '藕粉+蒸红薯+碎菜']
            },
            'snack': {
                'general': ['坚果+水果', '酸奶+燕麦', '全麦饼干+牛奶'],
                'diabetes': ['黄瓜条+无糖酸奶', '西红柿+核桃', '芹菜条+花生酱'],
                'hypertension': ['香蕉+杏仁', '苹果+核桃', '胡萝卜条+鹰嘴豆泥'],
                'elderly': ['蒸苹果+核桃', '藕粉+芝麻', '小米糊+南瓜子']
            }
        }

        # 扩展运动库 (增加注意事项)
        self.exercise_library = {
            'young': {
                'activities': ['跑步', '游泳', '健身操', '篮球', '羽毛球'],
                'notes': '运动前充分热身，注意补充水分'
            },
            'middle': {
                'activities': ['快走', '骑自行车', '瑜伽', '乒乓球', '跳舞'],
                'notes': '避免剧烈运动，注意关节保护'
            },
            'elderly': {
                'activities': ['太极拳', '散步', '八段锦', '气功', '柔力球'],
                'notes': '动作要缓慢，避免摔倒，最好有人陪同'
            },
            'diabetes': {
                'activities': ['有氧操', '水中运动', '骑自行车', '快走'],
                'notes': '避免空腹运动，携带糖果以防低血糖'
            },
            'hypertension': {
                'activities': ['瑜伽', '冥想', '散步', '太极'],
                'notes': '避免憋气动作，运动前后监测血压'
            },
            'cardiovascular': {
                'activities': ['散步', '轻度游泳', '柔瑜伽', '气功'],
                'notes': '强度不宜过大，出现不适立即停止'
            }
        }

        # 健康改善建议库
        self.health_tips = {
            'sleep': {
                'low': '保持7-8小时睡眠，建立规律作息',
                'medium': '改善睡眠环境，避免睡前使用电子设备',
                'high': '建议就医检查睡眠问题，可能需要专业干预'
            },
            'stress': {
                'low': '每日冥想10分钟，保持心情愉快',
                'medium': '尝试深呼吸练习，定期进行放松活动',
                'high': '建议寻求心理咨询或专业减压指导'
            },
            'diet': {
                'general': '均衡饮食，控制油盐糖摄入',
                'diabetes': '控制碳水化合物摄入，选择低GI食物',
                'hypertension': '低盐饮食，每日钠盐不超过5g',
                'cardiovascular': '增加膳食纤维，减少饱和脂肪摄入'
            },
            'herbal_tea': {
                'general': ['菊花茶(清热)', '枸杞茶(明目)', '大麦茶(助消化)'],
                'diabetes': ['桑叶茶', '玉米须茶', '苦瓜茶'],
                'hypertension': ['决明子茶', '山楂茶', '荷叶茶'],
                'cardiovascular': ['丹参茶', '三七花茶', '银杏叶茶']
            }
        }

        # 批处理大小
        self.batch_size = 1000

    def load_data(self, file_path="allData.csv"):
        """加载预测数据并自动修正异常值"""
        try:
            df = pd.read_csv(file_path)
            df = self.apply_corrections(df)
            return df
        except Exception as e:
            print(f"加载数据失败: {e}")
            return pd.DataFrame()

    def calculate_bmi(self, height, weight):
        """计算BMI指数"""
        if height > 0 and weight > 0:
            return round(weight / ((height / 100) ** 2), 2)
        return None

    def apply_corrections(self, df):
        """应用数据修正规则"""
        if not df.empty:
            # 修正生理指标范围
            for col in ['sleep_hours', 'blood_pressure_systolic',
                        'blood_pressure_diastolic', 'fasting_blood_sugar']:
                if col in df.columns:
                    min_val, max_val = self.correction_rules.get(col, (None, None))
                    if min_val is not None:
                        df[col] = df[col].clip(lower=min_val, upper=max_val)

            # 计算并修正BMI
            if 'height' in df.columns and 'weight' in df.columns:
                df['bmi'] = df.apply(lambda x: self.calculate_bmi(x['height'], x['weight']), axis=1)
                min_bmi, max_bmi = self.correction_rules['bmi']
                df['bmi'] = df['bmi'].clip(lower=min_bmi, upper=max_bmi)
                df['obesity'] = df['bmi'].apply(lambda x: 1 if x >= 28 else 0)

            # 修正无效分类值
            for col in ['physical_activity', 'dietary_habits']:
                if col in df.columns:
                    valid_values = self.correction_rules[col]
                    df[col] = df[col].apply(lambda x: x if x in valid_values else valid_values[0])

        return df

    def determine_risk_level(self, value, risk_type):
        """确定风险等级"""
        thresholds = self.risk_thresholds.get(risk_type, {})
        if not thresholds:
            return 'unknown'

        if risk_type == 'diabetes':  # 糖尿病风险评分处理方式不同
            if value < thresholds['low']:
                return 'low'
            elif value < thresholds['medium']:
                return 'medium'
            else:
                return 'high'
        else:  # 高血压和心脑血管概率处理
            if value < thresholds['low']:
                return 'low'
            elif value < thresholds['medium']:
                return 'medium'
            else:
                return 'high'

    def generate_personalized_diet(self, user_data):
        """生成个性化饮食计划(含早午晚加餐)"""
        age = user_data['age']
        has_diabetes = user_data.get('diabetes', 0) or user_data.get('Diabetes_Risk_Score', 0) >= 6
        has_hypertension = user_data.get('hypertension', 0) or user_data.get('Hypertension_Probability', 0) >= 0.6
        has_cardio = user_data.get('cardio', 0) or user_data.get('Cardiovascular_Probability', 0) >= 0.5

        # 确定饮食类型
        diet_type = 'general'
        if has_diabetes:
            diet_type = 'diabetes'
        elif has_hypertension:
            diet_type = 'hypertension'
        elif has_cardio:
            diet_type = 'cardiovascular'

        # 确定年龄组
        age_group = ''
        if age >= 60:
            age_group = 'elderly'

        # 生成7天饮食计划
        weekly_diet = {}
        for day in range(1, 8):
            # 优先使用特定类型的食物，如果没有则使用通用类型
            breakfast_options = self.food_library['breakfast'].get(diet_type, self.food_library['breakfast']['general'])
            if age_group:
                breakfast_options += self.food_library['breakfast'].get(age_group, [])

            lunch_options = self.food_library['lunch'].get(diet_type, self.food_library['lunch']['general'])
            if age_group:
                lunch_options += self.food_library['lunch'].get(age_group, [])

            dinner_options = self.food_library['dinner'].get(diet_type, self.food_library['dinner']['general'])
            if age_group:
                dinner_options += self.food_library['dinner'].get(age_group, [])

            snack_options = self.food_library['snack'].get(diet_type, self.food_library['snack']['general'])
            if age_group:
                snack_options += self.food_library['snack'].get(age_group, [])

            daily_meals = {
                'breakfast': np.random.choice(breakfast_options),
                'morning_snack': np.random.choice(snack_options),
                'lunch': np.random.choice(lunch_options),
                'afternoon_snack': np.random.choice(snack_options),
                'dinner': np.random.choice(dinner_options),
                'evening_snack': '无' if day % 2 else np.random.choice(snack_options)  # 隔天晚上加餐
            }
            weekly_diet[f'Day{day}'] = daily_meals

        return weekly_diet

    def generate_personalized_exercise(self, user_data):
        """生成个性化运动计划(含注意事项)"""
        age = user_data['age']
        has_diabetes = user_data.get('diabetes', 0) or user_data.get('Diabetes_Risk_Score', 0) >= 6
        has_hypertension = user_data.get('hypertension', 0) or user_data.get('Hypertension_Probability', 0) >= 0.6
        has_cardio = user_data.get('cardio', 0) or user_data.get('Cardiovascular_Probability', 0) >= 0.5

        # 确定年龄组
        if age < 40:
            age_group = 'young'
        elif age < 60:
            age_group = 'middle'
        else:
            age_group = 'elderly'

        # 基础运动选择
        exercises = self.exercise_library[age_group]['activities']
        notes = [self.exercise_library[age_group]['notes']]

        # 疾病特需调整
        if has_diabetes:
            exercises += self.exercise_library['diabetes']['activities']
            notes.append(self.exercise_library['diabetes']['notes'])
        if has_hypertension:
            exercises += self.exercise_library['hypertension']['activities']
            notes.append(self.exercise_library['hypertension']['notes'])
        if has_cardio:
            exercises += self.exercise_library['cardiovascular']['activities']
            notes.append(self.exercise_library['cardiovascular']['notes'])

        # 生成7天运动计划
        weekly_exercise = {}
        for day in range(1, 8):
            # 交替运动强度
            if day % 3 == 0:  # 每3天一次休息日或轻度运动
                activity = '休息日' if day % 6 == 0 else np.random.choice(['散步', '瑜伽', '冥想'])
                intensity = 'Light' if activity != '休息日' else 'None'
                duration = '30分钟' if activity != '休息日' else '充分休息'
            else:
                activity = np.random.choice(exercises)
                intensity = 'Moderate' if day % 2 else 'Light'
                duration = '45分钟' if intensity == 'Moderate' else '30分钟'

            weekly_exercise[f'Day{day}'] = {
                'activity': activity,
                'duration': duration,
                'intensity': intensity,
                'notes': '；'.join(notes)
            }

        return weekly_exercise

    def generate_health_improvement_tips(self, user_data):
        """生成健康改善建议(生活习惯、作息、花茶等)"""
        tips = {
            'lifestyle': [],
            'sleep': [],
            'diet': [],
            'herbal_tea': []
        }

        # 睡眠建议
        sleep_hours = user_data.get('sleep_hours', 7)
        if sleep_hours < 6:
            sleep_risk = 'high'
        elif sleep_hours < 7:
            sleep_risk = 'medium'
        else:
            sleep_risk = 'low'
        tips['sleep'].append(self.health_tips['sleep'][sleep_risk])

        # 压力建议
        stress_level = user_data.get('stress_level', 'Moderate')
        if stress_level == 'High':
            stress_risk = 'high'
        elif stress_level == 'Moderate':
            stress_risk = 'medium'
        else:
            stress_risk = 'low'
        tips['lifestyle'].append(self.health_tips['stress'][stress_risk])

        # 饮食类型建议
        has_diabetes = user_data.get('diabetes', 0) or user_data.get('Diabetes_Risk_Score', 0) >= 6
        has_hypertension = user_data.get('hypertension', 0) or user_data.get('Hypertension_Probability', 0) >= 0.6
        has_cardio = user_data.get('cardio', 0) or user_data.get('Cardiovascular_Probability', 0) >= 0.5

        if has_diabetes:
            tips['diet'].append(self.health_tips['diet']['diabetes'])
            tips['herbal_tea'].extend(self.health_tips['herbal_tea']['diabetes'])
        elif has_hypertension:
            tips['diet'].append(self.health_tips['diet']['hypertension'])
            tips['herbal_tea'].extend(self.health_tips['herbal_tea']['hypertension'])
        elif has_cardio:
            tips['diet'].append(self.health_tips['diet']['cardiovascular'])
            tips['herbal_tea'].extend(self.health_tips['herbal_tea']['cardiovascular'])
        else:
            tips['diet'].append(self.health_tips['diet']['general'])
            tips['herbal_tea'].extend(self.health_tips['herbal_tea']['general'])

        # 吸烟饮酒建议
        if user_data.get('smoking_status', 'No') == 'Yes':
            tips['lifestyle'].append('强烈建议戒烟，可寻求专业帮助')
        if user_data.get('alcohol_consumption', 'Moderate') == 'Heavy':
            tips['lifestyle'].append('减少酒精摄入，男性每日不超过2份，女性不超过1份')

        # 活动建议
        if user_data.get('PhysActivity', 1) == 0:
            tips['lifestyle'].append('增加日常活动量，如走楼梯代替电梯')

        return tips

    def generate_recommendations(self, user_data):
        """生成综合健康建议"""
        # 确定各项风险等级
        hypertension_prob = user_data.get('Hypertension_Probability', 0)
        cardio_prob = user_data.get('Cardiovascular_Probability', 0)
        diabetes_score = user_data.get('Diabetes_Risk_Score', 0)

        hypertension_risk = self.determine_risk_level(hypertension_prob, 'hypertension')
        cardio_risk = self.determine_risk_level(cardio_prob, 'cardiovascular')
        diabetes_risk = self.determine_risk_level(diabetes_score, 'diabetes')

        # 基础建议结构
        recommendations = {
            'risk_levels': {
                'hypertension': {'level': hypertension_risk, 'probability': hypertension_prob},
                'cardiovascular': {'level': cardio_risk, 'probability': cardio_prob},
                'diabetes': {'level': diabetes_risk, 'score': diabetes_score}
            },
            'diet_recommendations': [],
            'exercise_recommendations': [],
            'lifestyle_recommendations': [],
            'health_improvement_tips': self.generate_health_improvement_tips(user_data)
        }

        # 根据各项风险等级增强建议
        # 高血压相关建议
        if hypertension_risk == 'medium':
            recommendations['diet_recommendations'].append('减少钠盐摄入，每日不超过5g')
            recommendations['lifestyle_recommendations'].append('定期监测血压')
        elif hypertension_risk == 'high':
            recommendations['diet_recommendations'].append('严格低盐饮食，每日钠盐不超过3g')
            recommendations['lifestyle_recommendations'].append('建议尽快就医进行专业评估')

        # 心脑血管相关建议
        if cardio_risk == 'medium':
            recommendations['exercise_recommendations'].append('适度有氧运动，避免剧烈运动')
            recommendations['lifestyle_recommendations'].append('注意控制情绪波动，避免过度激动')
        elif cardio_risk == 'high':
            recommendations['exercise_recommendations'].append('运动需在医生指导下进行')
            recommendations['lifestyle_recommendations'].append('建议定期进行心脏检查')

        # 糖尿病相关建议
        if diabetes_risk == 'medium':
            recommendations['diet_recommendations'].append('控制碳水化合物摄入，选择低GI食物')
            recommendations['lifestyle_recommendations'].append('定期监测血糖水平')
        elif diabetes_risk == 'high':
            recommendations['diet_recommendations'].append('严格控制饮食，避免高糖食物')
            recommendations['lifestyle_recommendations'].append('建议就医进行糖耐量测试')

        # 生成详细计划
        recommendations['weekly_diet_plan'] = self.generate_personalized_diet(user_data)
        recommendations['weekly_exercise_plan'] = self.generate_personalized_exercise(user_data)

        return recommendations

    def process_all_users(self, file_path="allData.csv"):
        """处理所有用户数据并生成推荐（分批处理）"""
        df = self.load_data(file_path)
        if df.empty:
            print("没有可处理的数据！")
            return

        # 只取前3000条数据
        df = df.head(3000)
        total_users = len(df)
        batch_count = (total_users + self.batch_size - 1) // self.batch_size

        all_results = []
        processed_counts = []

        for batch_idx in tqdm(range(batch_count), desc="处理进度"):
            start_idx = batch_idx * self.batch_size
            end_idx = min((batch_idx + 1) * self.batch_size, total_users)
            batch_df = df.iloc[start_idx:end_idx]

            batch_results = []
            for idx, row in batch_df.iterrows():
                user_data = row.to_dict()
                recommendations = self.generate_recommendations(user_data)

                # 格式化输出
                formatted_rec = {
                    'user_id': idx,
                    'age': user_data['age'],
                    'gender': user_data['gender'],
                    'hypertension_risk': recommendations['risk_levels']['hypertension']['level'],
                    'hypertension_prob': recommendations['risk_levels']['hypertension']['probability'],
                    'cardio_risk': recommendations['risk_levels']['cardiovascular']['level'],
                    'cardio_prob': recommendations['risk_levels']['cardiovascular']['probability'],
                    'diabetes_risk': recommendations['risk_levels']['diabetes']['level'],
                    'diabetes_score': recommendations['risk_levels']['diabetes']['score'],
                    'diet_recommendations': '；'.join(recommendations['diet_recommendations']),
                    'exercise_recommendations': '；'.join(recommendations['exercise_recommendations']),
                    'lifestyle_recommendations': '；'.join(recommendations['lifestyle_recommendations']),
                    'sleep_tips': '；'.join(recommendations['health_improvement_tips']['sleep']),
                    'diet_tips': '；'.join(recommendations['health_improvement_tips']['diet']),
                    'herbal_tea_suggestions': '；'.join(recommendations['health_improvement_tips']['herbal_tea']),
                    'weekly_diet_plan': str(recommendations['weekly_diet_plan']),
                    'weekly_exercise_plan': str(recommendations['weekly_exercise_plan'])
                }
                batch_results.append(formatted_rec)

            all_results.extend(batch_results)
            processed_counts.append(len(batch_results))

        # 保存为CSV
        results_df = pd.DataFrame(all_results)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"health_recommendations_{timestamp}.csv"
        results_df.to_csv(output_file, index=False, encoding='utf-8-sig')

        print(f"\n处理完成！推荐已保存至 {output_file}")


if __name__ == "__main__":
    recommender = AdvancedHealthRecommender()
    recommender.process_all_users("allData.csv")
