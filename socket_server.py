import asyncio
import datetime
import random
import websockets
import eikon
import requests
import json



ric_codes = []
data_url = 'http://52.87.248.54/ric_codes'
app_id = 'CE9D75E3B5ECDE27DC3BDA'

eikon.set_app_id(app_id)

# async def consumer(ric_codes):
#     data = ric_codes.split(',')

# async def producer():
#     if not data:
#         return ''
#     rst, err = eikon.get_data(instruments=data, fields=['CF_LAST'])
#     return [str(d) for d in rst['CF_LAST']]

# async def consumer_handler(websocket, path):
#     while True:
#         ric_codes = await websocket.recv()
#         await consumer(ric_codes)

# async def producer_handler(websocket, path):
#     while True:
#         values = await producer()
#         await websocket.send(','.join(values))

# async def handler(websocket, path):
#     consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
#     producer_task = asyncio.ensure_future(producer_handler(websocket, path))
#     done, pending = await asyncio.wait(
#         [consumer_task, producer_task],
#         return_when=asyncio.FIRST_COMPLETED,
#     )

#     for task in pending:
#         task.cancel()

async def time(websocket, path):
	ric_codes = []
	while True:
		if not ric_codes:
			rst = requests.get(data_url)
			ric_codes = json.loads(rst.text)['data']
			ric_codes = [str(code) for code in ric_codes]
		# ric_codes = await websocket.recv()
		data, err = eikon.get_data(instruments=ric_codes, fields=['CF_LAST'])
		message = ','.join(['%.4f' % d for d in data['CF_LAST']])
		await websocket.send(message)
		await asyncio.sleep(0.1)

start_server = websockets.serve(time, '0.0.0.0', 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()