import asyncio

import api
async def main():
    baseUrl = 'http://cronicle.lan:3012'
    key = 'f64b28bd4d01d757809ba98cdc6297a3'
    rows = await api.get_jobs(baseUrl, key)
    print(list(map(lambda x: x, rows)))
    print(rows[0]['id'])
    print(await api.get_last_status(baseUrl, key, 'em7z72z0h5c'))

asyncio.run(main())