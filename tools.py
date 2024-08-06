from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()


def file_extraction(file_path):
    client = OpenAI(
        api_key=os.environ.get("Kimi_API_KEY"),
        base_url="https://api.moonshot.cn/v1",
    )
    file_object = client.files.create(file=Path(file_path), purpose="file-extract")
    file_content = client.files.content(file_id=file_object.id).text
    return file_content
