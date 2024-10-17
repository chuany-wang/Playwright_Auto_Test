import asyncio
import aiohttp
from sqlalchemy import and_

from common.init_sqlalchemy import db
from models.site.site_key_info import SiteKey
from models.site.site_func_info import SiteFunc


async def make_request(session, request_type, url, parameters, ):
    if request_type == 'post':
        async with session.post(url, data=parameters, timeout=10) as response:
            data = await response.json()
            return {"host": url, "data": data}
    elif request_type == 'get':
        async with session.get(url, params=parameters, timeout=10) as response:
            con_type = response.headers['Content-Type']
            if 'json' in con_type:
                data = await response.json()
                return {"host": url, "data": data}
            else:
                return await response.text()


async def retrieve_tokens(session, site_keys):
    login_url = "index.php?route=api/login&api_token="
    tasks = [
        asyncio.create_task(
            make_request(
                session,
                request_type='post',
                url=key.site_host + login_url,
                parameters={'username': 'Default', 'key': key.site_key}
            )
        ) for key in site_keys
    ]
    responses = await asyncio.gather(*tasks)
    tok_res = [
        {
            'host': response.get('host').replace(login_url, ""),
            'api_token': response.get('data').get('api_token')
        } for response in responses if isinstance(response.get('data'), dict)
    ]
    return tok_res


async def retrieve_theme(session, tokens):
    tasks = []
    task_theme = []
    checkurl = 'index.php'

    """请求获取config_theme"""
    for token in tokens:
        checkParams = {
            "route": 'api/v1/config/get',
            "keys": "config_theme",
            "api_token": token.get('api_token')
        }
        tasks.append(asyncio.create_task(
            make_request(session,
                         request_type='get',
                         url=token.get('host') + checkurl,
                         parameters=checkParams)
        ))
    theme_temp = await asyncio.gather(*tasks)

    for tok in tokens:
        for the in theme_temp:
            if tok.get('host') + checkurl == the.get('host'):
                config_theme = the.get('data').get('data').get('config_theme')
                fincheckParams = {
                    "route": 'api/v1/config/get',
                    "keys": f"config_theme,theme_{config_theme}_directory,theme_{config_theme}_mobile_directory,theme_kte_mobile_status",
                    "api_token": tok.get('api_token')
                }

                task_theme.append(asyncio.create_task(
                    make_request(session,
                                 request_type='get',
                                 url=the.get('host'),
                                 parameters=fincheckParams)
                ))
    responses = await asyncio.gather(*task_theme)
    theme_result = []
    for response in responses:
        config_theme = response.get('data').get('data').get('config_theme')
        host = response.get('host').replace(checkurl, "")
        pc_themes = response.get('data').get('data').get(f"theme_{config_theme}_directory")
        mobile_themes = response.get('data').get('data').get(f"theme_{config_theme}_mobile_directory")
        mobile_status = response.get('data').get('data').get("theme_kte_mobile_status")
        res_dict = {
            'host': host,
            'config_theme': config_theme,
            'pc_themes': pc_themes,
            'mobile_themes': mobile_themes,
            'mobile_status': mobile_status
        }
        theme_result.append(res_dict)

    return theme_result


async def retrieve_status(session, tokens, func_key):
    tasks = []
    checkurl = 'index.php'

    str_key = ','.join([i.func_key for i in func_key])

    for tok in tokens:
        fincheckParams = {
            "route": 'api/v1/config/get',
            "keys": str_key,
            "api_token": tok.get('api_token')
        }
        tasks.append(
            asyncio.create_task(
                make_request(session,
                             request_type='get',
                             url=tok.get('host') + checkurl,
                             parameters=fincheckParams)
            )
        )
    responses = await asyncio.gather(*tasks)
    func_result = []
    for response in responses:
        site_host = response.get('host').replace(checkurl, "")
        func_statu = response.get('data').get('data')
        for func, statu in func_statu.items():
            if statu:
                temp_dict = {'site_host': site_host, 'func_name': func, 'func_statu': statu}
            else:
                temp_dict = {'site_host': site_host, 'func_name': func, 'func_statu': "Null"}
            func_result.append(temp_dict)

    return func_result


async def retrieve_last_order(session, tokens):
    tasks = []
    for tok in tokens:
        fincheckParams = {
            "route": 'api/weline/order',
            "api_token": tok.get('api_token'),
            "state": 17,
            "page": 1,
            "pageSize": 1,
            "order": "DESC"
        }
        tasks.append(
            asyncio.create_task(
                make_request(session,
                             request_type='get',
                             url=tok.get('host'),
                             parameters=fincheckParams)
            )
        )
    responses = await asyncio.gather(*tasks)
    order_res = []
    for i in responses:
        data = i.get('data').get('items')
        if data:
            order_id = data[0].get('order_id')
        else:
            order_id = 'Null'
        res_dict = {
            'host': i.get('host'),
            'order_id': order_id,
        }
        order_res.append(res_dict)
    return order_res


async def retrieve_version(session, site_keys):
    version_url = "index.php"
    task_version = [
        asyncio.create_task(
            make_request(
                session,
                request_type='get',
                url=key.site_host + version_url,
                parameters={
                    'route': 'common/part/user/ajaxLoad'
                }
            )
        ) for key in site_keys
    ]
    responses = await asyncio.gather(*task_version)
    return responses


async def main(data, envir=None):
    async with aiohttp.ClientSession() as session:
        if envir == 'pro':
            site_keys = db.query(SiteKey).filter(
                and_(~SiteKey.site_host.like('%preview%'), ~SiteKey.site_host.like('%test%'))).all()
        elif envir == 'dev':
            site_keys = db.query(SiteKey).filter(SiteKey.site_host.like('%preview%')).all()
        else:
            site_keys = db.query(SiteKey).all()
        func_keys = db.query(SiteFunc).all()
        tokens = await retrieve_tokens(session, site_keys)
        if data == 'theme':
            result = await retrieve_theme(session, tokens)
        elif data == 'status':
            result = await retrieve_status(session, tokens, func_keys)
        elif data == 'order':
            result = await retrieve_last_order(session, tokens)
        elif data == 'version':
            result = await retrieve_version(session, site_keys)
    return result


def update_data(data, envir=None):
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(main(data=data, envir=envir))
    return result


if __name__ == '__main__':
    x = update_data(data="order", envir=None)
    print(x)
