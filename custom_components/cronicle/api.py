import aiohttp


async def get_jobs(baseUrl, key):
    async with aiohttp.ClientSession() as session:
        async with session.get(baseUrl + '/api/app/get_schedule/v1',
                               headers={'X-API-Key': key, 'Content-Type': 'application/json'}, timeout=10) as response:
            json_rsponse = await response.json()
            return json_rsponse['rows']


async def get_last_status(baseUrl, key, cronicle_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(baseUrl + '/api/app/get_event_history/v1',
                               headers={'X-API-Key': key, 'Content-Type': 'application/json'},
                               params={'id': cronicle_id, 'limit': 1, 'offset': 0}, timeout=10) as response:
            json_response = await response.json()
            return json_response['rows'][0]
