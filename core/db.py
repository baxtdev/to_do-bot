from core.config import DATABASE_URL
import json
from uuid import uuid4

async def create_task(data:dict):
    with open ('/Users/macpro2019/projects/to_do-bot/data.json','r+') as file:
        data_ = json.load(file)
        data_[str(uuid4())]=data
        file.seek(0)
        json.dump(data_,file,indent=4)


async def get_tasks(user_id:int):
    with open ('/Users/macpro2019/projects/to_do-bot/data.json','r+') as file:
        data_:dict = json.load(file)
        result = []
        for key,value in data_.items():
            if value["user_id"]==user_id:
                value['id']=key
                result.append(value)

    return result

async def delete_task(task_id:int):
    with open ('/Users/macpro2019/projects/to_do-bot/data.json','r') as file:
        data_:dict = json.load(file)
        data=data_.pop(task_id)
        with open ('/Users/macpro2019/projects/to_do-bot/data.json','w') as file:
            json.dump(data_,file,indent=4)       
    
