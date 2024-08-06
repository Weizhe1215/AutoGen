from autogen import ConversableAgent


def extraction_assistant(llm_config):
    agent = ConversableAgent(
        name="信息提取员",
        system_message="你是一个信息提取员，任务是将我需要的信息，从我给你的一大段文字中提取出来，并返回给我",
        llm_config=llm_config
    )
    return agent


def integrate_assistant(llm_config, requirements):
    agent = ConversableAgent(
        name="报告撰写员",
        system_message=f"你是一个报告撰写员，需要根据我发给你的字段，根据我的要求，详细的写出一份报告，并返回给我,以下是要求：不需要面面俱到，写出提供材料中包含的即可：{requirements}",
        llm_config=llm_config
    )
    return agent

