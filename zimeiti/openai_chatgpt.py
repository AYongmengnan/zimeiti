# import openai
# import json
# import openai_secret_manager
#
# # 连接OpenAI API
# secrets = openai_secret_manager.get_secret("openai")
# openai.api_key = secrets["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"]
# model_engine = "text-davinci-002"
# model = openai.Model(engine=model_engine)
#
#
# # 定义函数，使用OpenAI API优化文章标题
# def optimize_title(title):
#     prompt = f"优化以下文章标题：{title}"
#     response = model.generate(
#         prompt=prompt,
#         temperature=0.5,
#         max_tokens=60,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     output_title = response.choices[0].text.strip()
#     return output_title


# import openai
# openai.api_key = "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"
# # openai.Model(engine='text-davinci-002')
# def generate_response(prompt):
#     response = openai.Completion.create(
#         engine="text-davinci-002",
#         prompt=prompt,
#         temperature=0.5,
#         max_tokens=1024,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0
#     )
#     return response.choices[0].text.strip()
#
# while True:
#     prompt = input("请输入您的问题：")
#     response = generate_response(prompt)
#     print("答案：", response)



import openai
openai.api_key = "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"

def change_text(original_text):
    # 使用 text-davinci-002 模型进行文本优化
    model_engine = "text-davinci-002"
    prompt = f"请改进以下文本:\n{original_text}\n\n新文本:"
    response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, temperature=0.9)

    # 输出优化后的文本
    optimized_text = response.choices[0].text.strip()
    return optimized_text


if __name__ == '__main__':
    original_text = "蔡徐坤专辑搭售周边惹争议，“粉丝经济”能否撑起唱片复苏？"
    print(original_text)
    optimized_text = change_text(change_text)
    print(optimized_text)

