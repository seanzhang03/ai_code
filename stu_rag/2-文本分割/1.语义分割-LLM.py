import json
from pathlib import Path
import os
from langchain_community.document_loaders import TextLoader

# 读取华清远见.txt文本
file_path = os.path.join(Path(os.path.dirname(__file__)).parent, "datasets", "华清远见.txt")
# 创建文本加载器
loader = TextLoader(file_path, encoding='utf-8')
data = loader.load()
content = data[0].page_content

# 准备LLM
from langchain_openai import ChatOpenAI
import os

# 加载模型对象
llm = ChatOpenAI(
    # API_KEY，通过计算机的环境变量配置中读取
    api_key="sk-ws-H.PMMDXMY.mMS7.MEYCIQCRg3_Ti8ZBgWXDKkHkW5vAGcra4g8gGw5r-xuitvxTdgIhAPCeI4TaSG_kjPdTkwoGVIcn1KTIhTil-hW9FIlcVqYy",
    # 模型访问路径
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # 模型名称
    model="qwen3.7-max-2026-06-08",
    # 流式输出
    streaming=True,
)
# 准备问答数据
# 准备问答数据
messages = [
    {
        "role": "system",
        "content": """你是一个专业的文本语义分割引擎。你的唯一职责是将用户输入的文本按照语义完整性进行精准分割。

【核心规则】
1. 严禁输出任何开场白、问候语、解释说明、总结、注释或Markdown代码块标记。仅输出分割结果本身。
2. 分割点必须位于句子或段落的自然结束处，严禁截断正在表达中的语义单元。
3. 不得对原文进行摘要、改写、翻译、省略或添加任何原文中不存在的内容。
4. 自动过滤页眉、页脚、水印、乱码、广告、无关符号等噪声信息。
5. 若某片段语义不完整或无法独立表达一个完整意思，则将其与相邻片段合并。

【分割策略】
- 教程/教材类文本：按独立知识点、章节标题、操作步骤分割
- 文章/新闻类文本：按逻辑段落、论述层次分割
- 对话/问答类文本：按完整的问答轮次分割
- 代码类文本：按函数、类或功能模块分割
- 每个片段应包含一个完整且自洽的语义单元

【输出格式】
严格以JSON数组格式输出，每个元素为一个字符串片段。格式如下：
["片段1的完整内容", "片段2的完整内容", "片段3的完整内容"]

【示例】
输入：
"Python是一种解释型语言。它支持多种编程范式。接下来介绍变量。变量是存储数据的容器。Python中无需声明变量类型。"

输出：
["Python是一种解释型语言。它支持多种编程范式。", "接下来介绍变量。变量是存储数据的容器。Python中无需声明变量类型。"]

【再次强调】
只输出JSON数组，不输出任何其他内容。"""
    },
    {
        "role": "user",
        "content": f"请对以下文本执行语义分割，只输出JSON数组结果：\n\n{content}"
    }
]
# 调用LLM生成响应 --- 非流式响应,所谓非流式即不几个几个字符输出
response = llm.invoke(messages)
# 打印响应 --- response.content 获取到响应结果中的文本内容
print(response.content)
print(type(response.content))
data = json.loads(response.content)
for index, item in enumerate(data, start=1):
    print(f"片段{index}：{item}")

