from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()


# 文件提取
def file_extraction(file_path):
    client = OpenAI(
        api_key=os.environ.get("Kimi_API_KEY"),
        base_url="https://api.moonshot.cn/v1",
    )
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = client.files.content(file_id=file_object.id).text
    return file_content


# 根据输入生成一段话
def fill_placeholders(values, template) -> str:
    """
    将列表中的值依次填充到模板字符串中的多个占位符中。

    :param values: 一个包含要填充的值的列表。
    :param template: 一个包含多个占位符的模板字符串，占位符格式为 {placeholder}。
    :return: 一个填充后的字符串。
    """
    for value in values:
        template = template.replace("{placeholder}", value, 1)
    return template

