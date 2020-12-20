import aiohttp
#import asyncio
import pytest
import json


server_url = 'ws://localhost:8080'
pokemon = {'weight':69,'forms':[{'name':"bulbasaur",'url':'https://pokeapi.co/api/v2/pokemon-form/1/'}],'id':69}
invalid_input = {'ads':1,"asfnnv":[]}


async def send_to_server(data):
    async with aiohttp.ClientSession().ws_connect(server_url) as ws:
        await ws.send_json(data)
        async for message in ws:
            if message.type == aiohttp.WSMsgType.ERROR:
                print('Websocket connection closed with exception %s' % ws.exception())
            else:
                return message.data
            break


@pytest.mark.asyncio
async def test_happy_path():
    open_file_request = open('test_data_client/48.log', 'r')
    request = open_file_request.read()
    open_file_request.close()

    open_file_expected_result = open('test_data_server/48.log', 'r')
    expected_result = open_file_expected_result.read()
    open_file_expected_result.close()

    response = json.loads(await send_to_server(json.loads(request)))

    assert json.dumps(response) == expected_result


@pytest.mark.asyncio
async def test_response_is_json():
    response = json.dumps(await send_to_server(pokemon))

    assert json.loads(response)


@pytest.mark.asyncio
async def test_if_response_has_id_key():
    response = json.loads(await send_to_server(pokemon))
    assert 'id' in response


@pytest.mark.asyncio
async def test_if_response_has_name_key():
    response = json.loads(await send_to_server(pokemon))
    assert 'name' in response


@pytest.mark.asyncio
async def test_positive_case_boss():
    open_file_request = open('test_data_client/48.log', 'r')
    request = open_file_request.read()
    open_file_request.close()

    response = json.loads(await send_to_server(json.loads(request)))

    assert json.loads(request)['forms'][0]['name']+'_the_boss' == response['name']


@pytest.mark.asyncio
async def test_positive_case_feathers():
    open_file_request = open('test_data_client/50.log', 'r')
    request = open_file_request.read()
    open_file_request.close()

    response = json.loads(await send_to_server(json.loads(request)))

    assert "like_a_feather_" + json.loads(request)['forms'][0]['name'] == response['name']


@pytest.mark.asyncio
async def test_invalid_input():
    response = await send_to_server(invalid_input)
    assert response is None


@pytest.mark.asyncio
async def test_boundary_value_boss():
    open_file_request = open('test_data_client/50.log', 'r')
    request = open_file_request.read()
    open_file_request.close()

    invalid_weight_pokemon = json.loads(request)
    invalid_weight_pokemon['weight'] = 100
    response = json.loads(await send_to_server(invalid_weight_pokemon))

    assert response['name'] == json.loads(request)['name']


@pytest.mark.asyncio
async def test_boundary_value_feather():
    open_file_request = open('test_data_client/50.log', 'r')
    request = open_file_request.read()
    open_file_request.close()

    invalid_weight_pokemon = json.loads(request)
    invalid_weight_pokemon['weight'] = 50
    response = json.loads(await send_to_server(invalid_weight_pokemon))

    assert response['name'] == json.loads(request)['name']

