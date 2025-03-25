
import requests

cookies = {
    'uuid': 'b876e475a17a44498256.1739926697.1.0.0',
    '_lxsdk_cuid': '19111ce273cc8-0654b81b0eb26b-76574611-144000-19111ce273cc8',
    'iuuid': '2B3F12D9F6F0002A3ACB1441D39999C3935CFB0B242AAF86C7176521B12677CA',
    'ci': '55',
    'cityname': '%E5%8D%97%E4%BA%AC',
    '_lxsdk': '2B3F12D9F6F0002A3ACB1441D39999C3935CFB0B242AAF86C7176521B12677CA',
    'webp': '1',
    'i_extend': 'H__a100038__b1',
    '__utma': '74597006.1650529454.1739926706.1739926706.1739926706.1',
    '__utmz': '74597006.1739926706.1.1.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    'wm_order_channel': 'default',
    'swim_line': 'default',
    'utm_source': '',
    '_lx_utm': 'utm_source%3Dcn.bing.com%26utm_medium%3Dreferral%26utm_content%3D%252F',
    'WEBDFPID': '051x7x7uwu9054x2z8w3572w727zwu378072uvzv6v59795821zx099v-1741050506997-1728722952905COAMIMOa12a6b8169ee7736639f3ec62dbf984b6238',
    'terminal': 'i',
    'w_utmz': 'utm_campaign=(direct)&utm_source=5000&utm_medium=(none)&utm_content=(none)&utm_term=(none)',
    'openh5_uuid': '2B3F12D9F6F0002A3ACB1441D39999C3935CFB0B242AAF86C7176521B12677CA',
    'w_visitid': 'c044cc68-ec72-44b0-92ab-a984ac783bf5',
    'token': 'AgG-ImvBBHUR32UWm1k_T0B6mym-ir9MCrVJRlrMq3-9JfE7pz0va2qfbhKOkV2EgYMyG3YrGeyVXQAAAAASJwAAH421XM3n8t9MEVZ7f8DR1_0ImHm7wXhbxFOz1TGj-qObz-VhdxojnbQCKLY588Mo',
    'mt_c_token': 'AgG-ImvBBHUR32UWm1k_T0B6mym-ir9MCrVJRlrMq3-9JfE7pz0va2qfbhKOkV2EgYMyG3YrGeyVXQAAAAASJwAAH421XM3n8t9MEVZ7f8DR1_0ImHm7wXhbxFOz1TGj-qObz-VhdxojnbQCKLY588Mo',
    'oops': 'AgG-ImvBBHUR32UWm1k_T0B6mym-ir9MCrVJRlrMq3-9JfE7pz0va2qfbhKOkV2EgYMyG3YrGeyVXQAAAAASJwAAH421XM3n8t9MEVZ7f8DR1_0ImHm7wXhbxFOz1TGj-qObz-VhdxojnbQCKLY588Mo',
    'userId': '2876845534',
    'w_token': 'AgG-ImvBBHUR32UWm1k_T0B6mym-ir9MCrVJRlrMq3-9JfE7pz0va2qfbhKOkV2EgYMyG3YrGeyVXQAAAAASJwAAH421XM3n8t9MEVZ7f8DR1_0ImHm7wXhbxFOz1TGj-qObz-VhdxojnbQCKLY588Mo',
    'au_trace_key_net': 'default',
    'isIframe': 'false',
    '_lxsdk_s': '195598c116f-2b0-612-493%7C%7C69',
}

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://h5.waimai.meituan.com',
    'Referer': 'https://h5.waimai.meituan.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
    'mtgsig': '{"a1":"1.2","a2":1740964265809,"a3":"051x7x7uwu9054x2z8w3572w727zwu378072uvzv6v59795821zx099v","a5":"cdxwN2OcFLH4m7CzyBE/P70f/TEgMwX166n2p+Bl1RRZCwBxnK0P61W6MLTu614czW==","a6":"h1.8rfBLK32io3ehaFVGeraAqVIQvak/wqqSEBWhbkYnNbgsR+15GjRVwViv+UBRvpNpdOoar3yhxancYyMWzuBj4teSsxnOMHVoSNv6zg0vGYrdQ96wR/c6TGiQkCk1gvvADNCjcGR82dbGIIn2UhYva8RgrtOwGIvYOgMk+Sji+rhFITXYHlc08uLdKqf/XOdaFbB8iSan45Zi7dJJ3TCocoBOIgmyF1gRMmv952lFQBDUQzMhBplrVQe5ECBXLmrEUX4FLr2Y+K76+C0iwITyPHfqrGbScqjyZiHTYBoJ6jtzIWwgkYz9py/FCdZQTf5EPlG/JAjFhPcqNn3eb/90D/8GczeZonUn7lSBxO0S4+np6kboZLHoPkvp3nwaCmqHvnqn5hqCl/69fTUWqXhZKaWH2hka/z6HiLFnsoE+cfZi2Mzv2ULVUyRKYYIv4Np9","a8":"811d60f987bee56cf211fedde207f470","a9":"3.1.0,7,180","a10":"9c","x0":4,"d1":"64758d503cf72e9aabaf88395882a3cc"}',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

params = (
    ('_', '1740964265799'),
    ('yodaReady', 'h5'),
    ('csecplatform', '4'),
    ('csecversion', '3.1.0'),
)

data = {
  'optimus_code': '10',
  'optimus_risk_level': '71',
  'startIndex': '0',
  'cursor': '',
  'orderType': '0',
  'https://h5.waimai.meituan.com/waimai/mindex/olist': '',
  'wm_latitude': '31960803',
  'wm_longitude': '118746316',
  'wm_actual_latitude': '31964537',
  'wm_actual_longitude': '118779463',
  'wmUuidDeregistration': '0',
  'wmUserIdDeregistration': '0',
  'openh5_uuid': '2B3F12D9F6F0002A3ACB1441D39999C3935CFB0B242AAF86C7176521B12677CA',
  'uuid': '2B3F12D9F6F0002A3ACB1441D39999C3935CFB0B242AAF86C7176521B12677CA',
  '_token': 'eJx90m1vqjAUB/DvQrL7BiKlthRMlht8GOKcTjFXZVluUHlSHhSLCMv97rdgNFsylzTpj3970pMTPrjU2HAtCUgESAJ3clKuxUkN0JA5gaNHdkIQUGUEMYaKKnDrz5mMiUoEbpX+6XKtN0mWgKBC8F4lUxa8SexLkIDCoquR8i5AxFZ1y2CXOJ/S/bElij5u5HYQ2UEjcgKa2XFjnUTiJRKjIN4452pzWF8/l4SJF8S/3SRdO480zZxfK3u9+5ul4WNd99DUHuATW99Ws/wSMlwevcDhWMPRrGqYYFlQVIX1UUkFoBa+Cd2RVKt5E7wjWEu6CVyFlB9FbpK/qFkL3xGqhW5qfiN4k/RFuBa4I7ka2a4aGdvtz6MTtOqIXo9e2C/Hqo6BFzM5g4JuCRx7pTbxR0rYNhcQRt2uOZ16VidU091yPn/pmeejJ5oZoeX5aWSEEoY8aGblmIRljFH/vEi7PQdNMp+ayC1CPzQPdDTTk5MF3WlgaRIvP7uFDqLzM859lSycXToYtoF10CYF3Q8G225/b5uKfugkS9uiQzBYzSceRkZ7sXfUXZ4v9TI6aprf72X8cYin7mlVyj2yMMzEHRZ8Eg/LV3H5yp8hOBXyVj0dnFRcH/R0E/NFufO6Yr4frxRxa1F9PQeygTuFfLCV2B0RdzNr6x5aFVRf8Gm/E5G8M1MjpTDzolCMYWzp3L//Q10E7Q=='
}

response = requests.post('https://i.waimai.meituan.com/openh5/order/list', headers=headers, params=params, cookies=cookies, data=data)
response.json()

#NB. Original query string below. It seems impossible to parse and
#reproduce query strings 100% accurately so the one below is given
#in case the reproduced version is not "correct".
# response = requests.post('https://i.waimai.meituan.com/openh5/order/list?_=1740964265799&yodaReady=h5&csecplatform=4&csecversion=3.1.0', headers=headers, cookies=cookies, data=data)
