import yaml
import os

class PromptBuilder:
    @staticmethod
    def build_prompt(file_name):
        #获取yaml文件路径
        file_path = os.path.dirname(os.path.abspath(__file__))
        #读取文件
        with open(f"{file_path}/{file_name}","r",encoding="utf-8") as f:
            config = yaml.safe_load(f)
        print(config)
        #构建提示词
        prompt = f"""
            1.角色:{config["role"]}
            2.任务:{";".join(config["goal"])}\n
            3.要求:{";".join(config["rule"])}\n
            4.工具:{";".join(config["tool"])}\n
            5.输出:{";".join(config["output"]["rule"])}\n
        """
        return prompt
if __name__ == '__main__':
    rs = PromptBuilder.build_prompt("email_agent.yaml")
    print(rs)