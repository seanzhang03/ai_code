import requests
from dotenv import load_dotenv
import os
from langchain.tools import tool
from pydantic import BaseModel,Field
load_dotenv()

#获取地区的经纬度坐标
def get_location(address):
    params = {
        "key": os.getenv("AMAP_KEY"),  # 必填
        "address": address # 必填
    }
    rs = requests.get(
        url="https://restapi.amap.com/v3/geocode/geo?parameters",
        params=params
    )
    data = rs.json()
    return data["geocodes"][0]["location"]

#高德地图参数模型类
class AmapParams(BaseModel):
    start_location:str = Field(...,description="出发位置")
    end_location:str = Field(...,description="目的地")

@tool(args_schema=AmapParams)
def amap_tool(start_location:str,end_location:str)->str:
    """
        步行查询路线
    """
    try:
        #获取出发点和目的地的经纬度
        start = get_location(start_location)
        end = get_location(end_location)
        #定义参数
        params={
            "key":os.getenv("AMAP_KEY"),
            "origin":start,
            "destination":end
        }
        #发送请求
        rs = requests.get(
            url="https://restapi.amap.com/v3/direction/walking?parameters",
            params=params
        )
        #把响应数据转换成json
        data=rs.json()
        if data["status"] == "1":
            steps=data["route"]["paths"][0]["steps"]
            route = []
            for x in steps:
                route.append(x["instruction"])
            return "\n".join(route)
    except Exception as e:
        print(f"出现异常{e}")
        return "查询失败"

if __name__ == '__main__':
    rs=amap_tool.invoke({
        "start_location":"成都市宽窄巷子",
        "end_location":"成都市春熙路"
    })
    print(rs)