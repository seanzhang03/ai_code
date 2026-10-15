from http.cookiejar import debug

from langchain_core.messages import HumanMessage

from model.my_model import MyModel
from tools.send_email_tool import send_email_tool
from langchain.agents import create_agent
from prompt.prompt_builder import PromptBuilder

#agent工作原理：
# 1.LLM理解用户意图
# 2.判断是否需要调用tool
# 3.若为是，进行tool calling，tool执行完成后返回给observation，再给reasoning，最后给final answer
#定义一个函数
def get_agent(question):
    #1.创建大语言模型
    model = MyModel.get_line_model()
    #2.创建工具
    tools = [send_email_tool]
    #3.创建提示词
    prompt=PromptBuilder.build_prompt("email_agent.yaml")
    #4.创建智能体或者创建代理
    agent = create_agent(
        model=model,
        tools=tools,#工具
        system_prompt=prompt, #提示词
        debug=True #是否开启调试模式，生产环境下关闭
    )
    #5.提问
    rs = agent.invoke(
        {"messages":[{
            "role":"user",
            "content":question
        }]}
    ) #{'messages': [HumanMessage(content='请给2012761893@qq.com，发送一封邮件，通知其今晚来开会', additional_kwargs={}, response_metadata={}, id='7181983a-64f5-4556-9df8-fe8006edb38b'), AIMessage(content='', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 192, 'prompt_tokens': 434, 'total_tokens': 626, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 73, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cache_write_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'deepseek-v4-pro', 'system_fingerprint': None, 'id': '0217918720262260b63b37cbca791937f2f41fb0469576dc62b49', 'service_tier': 'default', 'finish_reason': 'tool_calls', 'logprobs': None}, id='lc_run--01a133e4-d40d-7443-aa95-432404da6fd0-0', tool_calls=[{'name': 'send_email_tool', 'args': {'name': 'send_email_tool', 'to_email': '2012761893@qq.com', 'subject': '会议通知', 'content': '您好，请于今晚准时参加会议，请提前安排好时间，谢谢！'}, 'id': 'call_b0c5f629b787413b92eb9a66', 'type': 'tool_call'}], invalid_tool_calls=[], usage_metadata={'input_tokens': 434, 'output_tokens': 192, 'total_tokens': 626, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 73}}), ToolMessage(content='邮件发送成功', name='send_email_tool', id='32fe0307-13ea-46c6-96eb-e126ed67e6e4', tool_call_id='call_b0c5f629b787413b92eb9a66'), AIMessage(content='邮件已成功发送至 **2012761893@qq.com** ✅\n\n- **邮件主题**：会议通知\n- **邮件内容**：您好，请于今晚准时参加会议，请提前安排好时间，谢谢！\n\n对方已收到开会通知，请知悉。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 97, 'prompt_tokens': 568, 'total_tokens': 665, 'completion_tokens_details': {'accepted_prediction_tokens': None, 'audio_tokens': None, 'reasoning_tokens': 40, 'rejected_prediction_tokens': None}, 'prompt_tokens_details': {'audio_tokens': None, 'cache_write_tokens': None, 'cached_tokens': 0}}, 'model_provider': 'openai', 'model_name': 'deepseek-v4-pro', 'system_fingerprint': None, 'id': '0217918720323250b63b37cbca791937f2f41fb0469576db91a18', 'service_tier': 'default', 'finish_reason': 'stop', 'logprobs': None}, id='lc_run--01a133e4-ed15-70c1-b570-a9becdf30333-0', tool_calls=[], invalid_tool_calls=[], usage_metadata={'input_tokens': 568, 'output_tokens': 97, 'total_tokens': 665, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 40}})]}

    #另一种提问方式
    # rs = agent.invoke({
    #     "messages":[
    #         HumanMessage(content=question)
    #     ]
    # })
    return rs["messages"][-1].content

if __name__ == '__main__':
    question = "请给2012761893@qq.com，发送一封邮件，通知其今晚来开会"
    rs=get_agent(question)
    print(rs)

    #所有的组件，都要遵守Runnable接口规范，invoke，stream，ainvoke，astream
    # invoke 同步非流式，同步调用模型
    # stream 同步流式，模型生成一个token，程序立即返回一个token，接收内容时要用循环一个一个接收
    # ainvoke 异步非流式
    # astream 异步流式