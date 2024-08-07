Strategy_requirements_dic = {
    "Simple Quant Strategy": "以下是量化策略的模板，以下内容都需要在段落中进行体现, 管理人的量化模型和因子上需要写详细一些："
                             "1. 管理⼈量化策略的整体思路，这部分主要说明管理人的量化策略的核心思路"
                             "2. 管理⼈的因⼦组成百分比和因子的总数量, 以及管理人对对应因子的描述。"
                             "3. 管理⼈的因⼦挖掘⽅法, 具体需要判断是人工手工挖掘，还是使用了机器学习，并详述他们用到的算法和方法论"
                             "4. 管理⼈的因⼦处理⽅法, 具体需要判断其对因子的合成方法，处理方法等（如有），并详述他们用到的算法和方法论"
                             "5. 管理⼈的量化模型，需要明确提示是线性还是机器学习模型或者是两者都有及其偏好。并详述他们的建模方法论，包括使用了何种模型，方法或算法进行了何种任务"
                             "6. 管理⼈的因⼦⼊库条件, 即管理人的新因子入库标准和流程 "
                             "7. 管理⼈的具体执⾏, 对股票进行了什么处理，有无使用算法下单等，最终持有了多少个股，指数内占比，行业偏离度，风格偏离度，年化双边换手率多少倍。"
                             "8. 管理⼈的对冲⽅法（如有）， 使⽤什么进⾏对冲, 有⽆敞⼝"
}

Strategy_prompt_dic = {
    "Simple Quant Strategy": [
        '管理⼈量化策略的整体思路, 例如，是偏强逻辑为主, 对因⼦的可解释性有很⾼的要求；还是偏暴力挖掘为主，使用机器学习较多',
        '从文件中提取出管理人的策略中的因子组成和因子数量,包括量价类,基本面，另类因子占比多少，以及因子的总数',
        '从文件中提取出管理人对其不同因子类型的解释（如有），具体来说主要是不同因子是基于哪些数据得出的，不要编造，只能抽取提供信息中有的内容。如果没有详细说明，则返回无',
        '从文件中提取出管理人的建模方法，需要明确提示是线性还是机器学习模型或者是两者都有及其偏好。其中线性模型包括：排序打分和简单回归，详述他们的建模方法论, '
        '并提取出他们使用了的算法和用途。不要把因子挖掘的部分写进去，只需要说建模',
        '从文件中提取出管理人的新因子入库条件，包括但不限于在模拟盘中观察的时间, 衡量指标如夏普，ICIR等，以及其他的措施等。不要编造，只能抽取提供信息中有的内容。如果没有详细说明，则返回无',
        '从文件中提取出管理人的具体操作，例如有无使用自研/外部的下单算法，不同策略的持股数是多少，年化双边换手率多少倍，行业偏离度，风格偏离度，barra风格因子暴露等'
    ]
}

Other_prompt_dic = {
    "中性多头/对冲端": "管理人的多头端是 {placeholder}， 使用 {placeholder}进行对冲，留{placeholder}的风险敞口."
}
