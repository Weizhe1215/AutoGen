from autogen import ConversableAgent

extraction_assistant = ConversableAgent(
        name = "信息提取员",
        system_message = "你是一个信息提取员，任务是将我需要的信息，从我给你的一大段文字中提取出来，并返回给我",
        llm_config = weak_config
    )

