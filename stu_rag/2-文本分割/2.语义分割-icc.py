from pathlib import Path
import os
from modelscope.outputs import OutputKeys
from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from langchain_community.document_loaders import TextLoader

# pipeline：封装为管道，调用的时候直接可以通过输出得到输出，按照封装流程执行即可
p = pipeline(
    # 任务类型。Tasks.document_segmentation：文本分割任务
    task=Tasks.document_segmentation,
    # 模型存储路径 -- 只需要给路径即可，模型名字不需要再写，使用的模型是 iic/nlp_bert_document-segmentation_chinese-base
    model='E:/ai_code/models/nlp_bert_document-segmentation_chinese-base',
    # 模型版本
    model_revision='master',
)

# 读取华清远见.txt文本
file_path = os.path.join(Path(os.path.dirname(__file__)).parent, "datasets", "华清远见.txt")
# 创建文本加载器
loader = TextLoader(file_path, encoding='utf-8')
data = loader.load()
content = data[0].page_content

# 调用管道，分割数据，得到结果
result = p(documents=content)[OutputKeys.TEXT]
# 输出结果 --- 整个分割是一段文本
print(result)
# 处理结果
split_data = result.split('\n')
for index, item in enumerate(split_data, start=1):
    if item.strip():    # 去除空行
        print(f"第{index}个块：{item}")


