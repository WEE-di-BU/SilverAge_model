from openai import OpenAI

# 初始化 OpenAI 客户端
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="7a412c00-bdc3-4b1a-beef-b1bf4d5f33d6",
)

# 维护对话历史记录
history = [
    {"role": "system", "content": "你是医疗相关方面的智能助手，需要耐心细致富有同理心地以聊天的方式解答用户的提问。"}
]


def medical_chat(chat_text, guide_words=""):
    global history  # 使用全局变量来维护对话历史

    # 添加用户输入到历史记录
    user_message = {"role": "user", "content": f"{guide_words}：{chat_text}"}
    history.append(user_message)

    # 调用 API 并传递完整的历史记录
    response = client.chat.completions.create(
        model="doubao-1-5-lite-32k-250115",
        messages=history,  # 传递完整的历史记录
    )

    # 获取助手的回复
    assistant_reply = response.choices[0].message.content

    # 将助手的回复添加到历史记录
    assistant_message = {"role": "assistant", "content": assistant_reply}
    history.append(assistant_message)

    return assistant_reply


def medical_chat_stream(chat_text, guide_words=""):
    global history  # 使用全局变量来维护对话历史

    # 添加用户输入到历史记录
    user_message = {"role": "user", "content": f"{guide_words}：{chat_text}"}
    history.append(user_message)

    # 调用 API 并传递完整的历史记录
    response = client.chat.completions.create(
        model="doubao-1-5-lite-32k-250115",
        messages=history,  # 传递完整的历史记录
        stream=True,
    )

    # 处理解析流式响应
    assistant_reply = ""  # 用于存储助手的完整回复
    for chunk in response:
        if hasattr(chunk.choices[0], 'delta') and hasattr(chunk.choices[0].delta, 'content'):
            content = chunk.choices[0].delta.content
            print(content, end='')  # 实时打印流式内容
            assistant_reply += content  # 拼接流式内容

    # 将助手的回复添加到历史记录
    assistant_message = {"role": "assistant", "content": assistant_reply}
    history.append(assistant_message)

    return assistant_reply


def run_doubao_chat(stream=True):
    print("智能医疗助手已启动，请开始对话（输入 'q' 结束对话）：")
    while True:
        chat_text = input("> ")
        if chat_text.lower() == "q":
            print("对话已结束，感谢使用！")
            break

        # 选择非流式或流式方式
        if stream:
            medical_chat_stream(chat_text)
            print()
        else:
            print(medical_chat(chat_text))


if __name__ == '__main__':
    stream_flag = True
    run_doubao_chat(stream_flag)