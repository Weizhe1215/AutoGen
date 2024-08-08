import gradio as gr
from docx import Document
import LLM_configs
import Prompt_dics
# 假设 LLM_configs, Prompt_dics 和 quant_dict 已经定义
from Agents import *
from tools import *

import gradio as gr
from docx import Document
from io import BytesIO

quant_dict = {
    'quant_idea': [],
    'factor_composition': [],
    'factor_explanation': [],
    'model_explanation': [],
    'factor_update': [],
    'strategy_execution': []
}


def file_extraction(file):
    # 读取 DOCX 文件内容
    file_path = file.name  # 获取文件路径
    document = Document(file_path)
    file_content = ""
    for para in document.paragraphs:
        file_content += para.text + "\n"
    return file_content


def report_writing(text, old_report_part, weak_config, strong_config, prompts, component_dict, requirements, updating):
    extraction_agent = extraction_assistant(weak_config)
    integrate_agent = integrate_assistant(strong_config, requirements)

    for prompt, component in zip(prompts, list(component_dict.keys())):
        reply = extraction_agent.generate_reply(messages=[{"content": text, "role": "system"},
                                                          {"content": prompt, "role": "user"}])
        component_dict[component].append(reply)

    final_report = integrate_agent.generate_reply(messages=[{"content": str(component_dict), "role": "system"},
                                                            {
                                                                "content": "按需求生成报告，不要分段，写成一整段，要求逻辑清晰，细节完整，长度越长越好，但不要有过多的你自由发挥的解释，客观记录为主, 不要出现评价语言，例如“这体现了XXXX",
                                                                "role": "user"}])
    non_updating_report = final_report

    if updating:
        final_report = integrate_agent.generate_reply(messages=[
            {"content": "旧报告: " + old_report_part + " 新报告: " + str(final_report), "role": "system"},
            {
                "content": "你是一个报告审查和撰写专员，现在你有一篇旧报告和一篇新报告，你要做的是在旧报告的基础上，判断新报告中的增量信息，并将新报告中的增量信息与旧报告中的现有信息相结合，完成一篇更新的报告，如果两个报告中对某一个地方有冲突，则以新报告为准。",
                "role": "system"},
            {
                "content": "按需求生成报告，不要分段，写成一整段，要求逻辑清晰，细节完整. 长度越长越好，但不要有过多的你自由发挥的解释，客观记录为主, 不要出现评价语言，例如“这体现了XXXX",
                "role": "user"}])

    return final_report, non_updating_report, component_dict, []

def report_rewrite(feedback, report,config):
    report_modify_agent = report_modify(config)
    new_report = report_modify_agent.generate_reply(messages = [{"content": "修改要求："+feedback+"，其他的一个字都不能改", "role": "system"},
                                                                      {"content": "这是报告:"+report, "role": "system"},
                                                                      {"content": "按照要求，对报告进行修改", "role": "user"}])
    return new_report


with gr.Blocks() as demo:
    with gr.Tab("更新尽调报告"):
        with gr.Row():
            dropdown = gr.Dropdown(choices=["股票量化"], label="选择功能")

        with gr.Row(visible=False) as quant_row:
            with gr.Column():
                quant_file_uploader = gr.File(label="上传文件")
                quant_button = gr.Button("生成")
                quant_update = gr.Textbox(label="请输入修改要求")
                quant_updated_report_button = gr.Button("更新")
            quant_textbox = gr.Textbox(label="输入上次的尽调报告", lines=15)
            quant_output = gr.Textbox(label="尽调报告结果", interactive=False, lines=15)




        def update_ui(choice):
            if choice == "股票量化":
                return gr.update(visible=True)
            return gr.update(visible=False)


        dropdown.change(update_ui, inputs=dropdown, outputs=quant_row)


        def on_generate_clicked(file, old_report_part):
            if file:
                text = file_extraction(file)  # 提取文件内容
                # 调用 report_writing 函数
                Ali_report, first_Ali_report, Quant_component_dic, cost_list = report_writing(
                    text, old_report_part,
                    LLM_configs.Qwen_weak_llm_config,
                    LLM_configs.Qwen_strong_llm_config,
                    Prompt_dics.Strategy_prompt_dic['Simple Quant Strategy'],
                    quant_dict,
                    Prompt_dics.Strategy_requirements_dic['Simple Quant Strategy'],
                    updating=True
                )
                return Ali_report
            return "请上传一个文件。"

        def on_update_clicked(input_message, generated_report):
            new_report = report_rewrite(input_message, generated_report,LLM_configs.Qwen_strong_llm_config)
            return new_report

        quant_button.click(on_generate_clicked, inputs=[quant_file_uploader, quant_textbox], outputs=quant_output)
        quant_updated_report_button.click(on_update_clicked, inputs=[quant_update, quant_output], outputs=quant_output)

demo.launch()
