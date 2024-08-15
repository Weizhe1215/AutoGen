import LLM_configs
import Prompt_dics
from tools import *
from Interface_functions import *

import gradio as gr
from docx import Document

quant_dict = {
    'quant_idea': [],
    'factor_composition': [],
    'factor_explanation': [],
    'model_explanation': [],
    'factor_update': [],
    'strategy_execution': []
}

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
                final_report, draft_report, component_dic, cost_list = report_writing(
                    text, old_report_part,
                    LLM_configs.kimi_weak_llm_config,
                    LLM_configs.kimi_strong_llm_config,
                    Prompt_dics.Strategy_prompt_dic['Simple Quant Strategy'],
                    quant_dict,
                    Prompt_dics.Strategy_requirements_dic['Simple Quant Strategy'],
                    updating=True
                )
                return final_report
            return "请上传一个文件。"


        def on_update_clicked(input_message, generated_report):
            new_report = report_rewrite(input_message, generated_report, LLM_configs.Qwen_strong_llm_config)
            return new_report


        quant_button.click(on_generate_clicked, inputs=[quant_file_uploader, quant_textbox], outputs=quant_output)
        quant_updated_report_button.click(on_update_clicked, inputs=[quant_update, quant_output], outputs=quant_output)

demo.launch()
