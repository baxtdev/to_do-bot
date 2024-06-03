import aiohttp
import json
import requests


async def get(url,user_id):
    headers = {'Content-type': 'application/json', 'X-Bot-User': f'{user_id}'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers) as response:

                if response.status == 200:
                    data = await response.json()
                    return data

                return None
            
        except aiohttp.ClientError as e:
            return None
        

async def post(url,data,user_id):
    headers = {'Content-type': 'application/json','X-Bot-User': f'{user_id}'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, data=json.dumps(data), headers=headers) as response:

                if response.status == 200:
                    data = await response.json()
                    return data

                return None
            
        except aiohttp.ClientError as e:
            return None
        


async def update(url,data,user_id,task_id):
    headers = {'Content-type': 'application/json','X-Bot-User': f'{user_id}'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.put(url, data=json.dumps(data), headers=headers) as response:

                if response.status == 200:
                    data = await response.json()
                    return data

                return None
            
        except aiohttp.ClientError as e:
            return None
        

async def delete(url,user_id,task_id):
    headers = {'Content-type': 'application/json','X-Bot-User': f'{user_id}'}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(url, headers=headers) as response:

                if response.status == 200:
                    data = await response.json()
                    return data

                return None
            
        except aiohttp.ClientError as e:
            return None        
            