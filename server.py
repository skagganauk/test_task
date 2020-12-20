import aiohttp
from aiohttp import web
#import asyncio
import json



def pokemon_parser(pokemon):
    json_pokemon = json.loads(pokemon)
    json_pokemon_response = {}
    json_pokemon_response['weight'] = json_pokemon['weight']
    json_pokemon_response['id'] = json_pokemon['id']

    if json_pokemon_response['weight'] > 100:
        json_pokemon_response['name'] = json_pokemon['forms'][0]['name'] + '_the_boss'
    elif json_pokemon_response['weight'] < 50:
        json_pokemon_response['name'] = 'like_a_feather_' + json_pokemon['forms'][0]['name']
    else:
        json_pokemon_response['name'] = json_pokemon['forms'][0]['name']

    logger = open('server_logs/' + str(json_pokemon_response['id'])+'.log', "w")
    del json_pokemon_response['weight']
    logger.write(json.dumps(json_pokemon_response))

    logger.close()

    return json_pokemon_response


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for message in ws:
        pokemon = pokemon_parser(message.data)
        pokemon_json_response = json.dumps(pokemon)
        await ws.send_str(pokemon_json_response)

    if message.type == aiohttp.WSMsgType.ERROR:
            print('Websocket connection closed with exception %s' % ws.exception())

    print('websocket connection closed')

    return ws


app = web.Application()
app.add_routes([web.get('/', websocket_handler)])
print("server running")
web.run_app(app)



