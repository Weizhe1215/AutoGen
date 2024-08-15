from docx import Document
import Agents as Ag
from typing import *
import httpx
from openai import OpenAI
from dotenv import load_dotenv
import os

# 读取 环境中的 kimi api key并创建 client
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("Kimi_API_KEY"),
    base_url="https://api.moonshot.cn/v1",
)


# 标准的 openai 格式回复
def open_ai_generate_reply(messages, llm_config):
    response = client.chat.completions.create(
        model=llm_config["model"],  # 使用弱配置的模型
        messages=messages
    )
    return response.choices[0].message["content"]


# 读取 docx文件的函数
def file_extraction(file):
    # 读取 DOCX 文件内容
    file_path = file.name  # 获取文件路径
    document = Document(file_path)
    file_content = ""
    for para in document.paragraphs:
        file_content += para.text + "\n"
    return file_content


def upload_and_cache_file(text: str, cache_tag: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    将文本内容上传并缓存。
    """
    messages = [{"role": "system", "content": text}]

    if cache_tag:
        r = httpx.post(f"{client.base_url}caching",
                       headers={
                           "Authorization": f"Bearer {client.api_key}",
                       },
                       json={
                           "model": "moonshot-v1",
                           "messages": messages,
                           "ttl": 100,
                           "tags": [cache_tag],
                       })

        if r.status_code != 200:
            raise Exception(r.text)

        return [{
            "role": "cache",
            "content": f"tag={cache_tag};reset_ttl=300",
        }]
    else:
        return messages


# 撰写报告的函数
def report_writing(text, old_report_part, weak_config, strong_config, prompts, component_dict, requirements, updating):
    cache_tag = "quant_cache"  # 为缓存设置一个唯一标识
    file_messages = upload_and_cache_file(text, cache_tag)

    extraction_agent = Ag.extraction_assistant(weak_config)
    integrate_agent = Ag.integrate_assistant(strong_config, requirements)

    for prompt, component in zip(prompts, list(component_dict.keys())):
        messages = [
            *file_messages,
            {"content": prompt, "role": "user"}
        ]
        print(messages)
        reply = extraction_agent.generate_reply(messages=messages)
        component_dict[component].append(reply)

    final_report = integrate_agent.generate_reply(messages=[{"content": str(component_dict), "role": "system"},
                                                            {
                                                                "content": "按需求生成报告，不要分段，写成一整段，要求逻辑清晰，细"
                                                                           "节完整，长度越长越好，但不要有过多的你自由发挥的解释，"
                                                                           "客观记录为主, 不要出现评价语言，例如“这体现了XXXX",
                                                                "role": "user"}])
    non_updating_report = final_report

    if updating:
        final_report = integrate_agent.generate_reply(messages=[
            {"content": "旧报告: " + old_report_part + " 新报告: " + str(final_report), "role": "system"},
            {
                "content": "你是一个报告审查和撰写专员，现在你有一篇旧报告和一篇新报告，你要做的是在旧报告的基础上，判断新报告中的增量信息"
                           "，并将新报告中的增量信息与旧报告中的现有信息相结合，完成一篇更新的报告，如果两个报告中对某一个地方有冲突，则以新报告为准。",
                "role": "system"},
            {
                "content": "按需求生成报告，不要分段，写成一整段，要求逻辑清晰，细节完整. 长度越长越好，但不要有过多的你自由发挥的解释，客观记录为主, 不要出现评价语言，例如“这体现了XXXX",
                "role": "user"}])

    return final_report, non_updating_report, component_dict, []


# 更新报告的函数
def report_rewrite(feedback, report, config):
    report_modify_agent = Ag.report_modify(config)
    new_report = report_modify_agent.generate_reply(
        messages=[{"content": "修改要求：" + feedback + "，其他的一个字都不能改", "role": "system"},
                  {"content": "这是报告:" + report, "role": "system"},
                  {"content": "按照要求，对报告进行修改", "role": "user"}])
    return new_report
