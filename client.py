import aiohttp
import asyncio
import json
pokemon_url = 'https://pokeapi.co/api/v2/pokemon?limit=50'
socket_url = 'ws://localhost:8080'


def pokemon_filter(pokemon_type):
    if len(pokemon_type) < 2:
        return False
    is_fire_or_grass = False
    for each_type in pokemon_type:
        if each_type['type']['name'] == 'fire' or each_type['type']['name'] == 'grass':
            is_fire_or_grass = True

    return is_fire_or_grass


def pokemon_name_parser(single_pokemon):
    name = single_pokemon['forms'][0]['name']
    return name


async def send_pokemon(pokemon, ws):
    await ws.send_json(pokemon)
    async for message in ws:
        if message.type == aiohttp.WSMsgType.ERROR:
            print('Websocket connection closed with exception %s' % ws.exception())
        else:
            print(message.data)
        break


async def fetch_pokemon():
    async with aiohttp.ClientSession() as session:
        resp = await session.get(pokemon_url)
        json_resp = await resp.json()
        pokemon = json_resp['results']
        await session.close()

        async with aiohttp.ClientSession().ws_connect(socket_url) as ws:

            for single_pokemon in pokemon:
                async with aiohttp.ClientSession() as pokemon_session:
                    pokemon_resp = await pokemon_session.get(single_pokemon['url'])
                    single_pokemon_json = await pokemon_resp.json()
                    await pokemon_session.close()

                    pokemon_type = single_pokemon_json['types']
                    if pokemon_filter(pokemon_type):

                        print("Pokemon {} wasn't sent to server".format(pokemon_name_parser(single_pokemon_json)))

                    else:
                        await send_pokemon(single_pokemon_json, ws)
                        logger = open('test_data_client/' + str(single_pokemon_json['id']) + '.log', "w")
                        logger.write(json.dumps(single_pokemon_json))
                        logger.close()

            await ws.close()


asyncio.run(fetch_pokemon())






