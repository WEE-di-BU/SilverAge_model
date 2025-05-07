# # from openai import OpenAI
#
# # 替换为你的DeepSeek API Key
# api_key = "sk-eecd41ca530f4865b980aedaa8a6f19b"
#
# # 初始化客户端
# client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
#
# # 调用DeepSeek API进行体检报告解读
# def interpret_health_report(report_text, guide_words=""):
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {"role": "system",
#              "content": "你是一个帮助解读健康报告的助手。使用中文回答，语言简单易懂，避免专业术语。举生活常识来解释专业术语，比如胆固醇偏高可能就是猪肉吃多了等。像和普通人聊天一样解释每个部分。"},
#             {"role": "user", "content": f"请用中文详细解读以下健康报告，给出一些参考建议，像和普通人聊天一样解释每个部分,{guide_words}：{report_text}"}
#         ],
#         stream=False  # 非流式输出
#     )
#     return response.choices[0].message.content
#
# # 调用DeepSeek API进行体检报告解读（流式输出）
# def interpret_health_report_stream(report_text, guide_words=""):
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {"role": "system",
#              "content": "你是一个帮助解读健康报告的助手。使用中文回答，语言简单易懂，避免专业术语。举生活常识来解释专业术语，比如胆固醇偏高可能就是猪肉吃多了等。像和普通人聊天一样解释每个部分。"},
#             {"role": "user", "content": f"请用中文详细解读以下健康报告，给出一些参考建议，像和普通人聊天一样解释每个部分,{guide_words}：{report_text}"}
#         ],
#         stream=True  # 流式输出
#     )
#     # 处理解析流式响应
#     for chunk in response:
#         if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
#             content = chunk.choices[0].delta.content
#             print(content, end='')  # 实时打印流式内容
#
#
# def run_deepseek_reporter(report_text, stream_flag=False):
#     if stream_flag:
#         # 示例：上传体检报告文本并获取流式解读
#         print("体检报告解读结果（流式输出）：")
#         interpret_health_report_stream(report_text)
#     else:
#         # 示例：上传体检报告文本并获取解读
#         interpretation = interpret_health_report(report_text)
#         print("体检报告解读结果：")
#         print(interpretation)
#
#
#
#
# if __name__ == '__main__':
#     report_text = """
#         基础信息
#
#         年龄：56岁
#         性别：男性
#         地区：农村
#         收入水平：中等
#         健康状况
#
#         高血压：无
#         糖尿病：有
#         胆固醇水平：211 mg/dL
#         肥胖：无
#         腰围：83 cm
#         家族史：无
#         生活习惯
#
#         吸烟状态：从不吸烟
#         饮酒量：无
#         运动量：高
#         饮食习惯：不健康
#         空气质量暴露：中等
#         压力水平：中等
#         睡眠时长：5.97小时（平均）
#         医疗指标
#
#         收缩压：113 mmHg
#         舒张压：62 mmHg
#         空腹血糖：173 mg/dL
#         高密度脂蛋白胆固醇（HDL-C）：48 mg/dL
#         低密度脂蛋白胆固醇（LDL-C）：121 mg/dL
#         甘油三酯：101 mg/dL
#         心电图结果：正常
#         病史与用药
#
#         既往心脏病：无
#         用药情况：无
#         参与免费筛查：否
#         曾患心脏病：否
#         """
#
#     stream_flag = True
#     run_deepseek_reporter(report_text, stream_flag)