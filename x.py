"""
Author: liupeitao sudolovelnpctly6869@outlook.com
Date: 2024-11-28 17:21:01
LastEditors: liupeitao sudolovelnpctly6869@outlook.com
LastEditTime: 2024-11-28 17:21:13
FilePath: /spider-android/x.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
"""

import requests

headers = {
    "accept": "*/*",
    "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "cache-control": "no-cache",
    "cookie": 'guest_id=v1%3A173156521177562101; night_mode=2; guest_id_marketing=v1%3A173156521177562101; guest_id_ads=v1%3A173156521177562101; g_state={"i_l":0}; kdt=XDuuwsanKqHihogUHgpLEqbhR9K9otoTIN9oIpkF; auth_token=ca8daaa8c5143608bfddcfe3eecbadb932b7ead5; ct0=8cef223e71458e4e51c7c0088b5ce5ac9442da63cfc8d6858d8407e28340064701d9e310f233bc67ab672f1676d45ea9a8f441888d6eafeafd91a1490a4ecb96aefc1376403711232de0c7abfbeea886; twid=u%3D1860953157419028480; personalization_id="v1_OCI1Rjr8SJkrZ4siEP92Cg=="; lang=en',
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://x.com/messages/1798995068067663872-1860953157419028480",
    "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "x-client-transaction-id": "6uxroY1PFxZlmuN/ZqZpO7WaX2Cp9L4g9yN3w8H7I5Ilu/AxsHcE+mFaDe2tzLm/HP07EuhtRAD/MUOSuKAuWj2wDvmj6Q",
    "x-client-uuid": "3d584b67-d890-477b-8d5f-e9ad5b23201b",
    "x-csrf-token": "8cef223e71458e4e51c7c0088b5ce5ac9442da63cfc8d6858d8407e28340064701d9e310f233bc67ab672f1676d45ea9a8f441888d6eafeafd91a1490a4ecb96aefc1376403711232de0c7abfbeea886",
    "x-twitter-active-user": "yes",
    "x-twitter-auth-type": "OAuth2Session",
    "x-twitter-client-language": "en",
}

params = (
    ("context", "FETCH_DM_CONVERSATION"),
    ("include_profile_interstitial_type", "1"),
    ("include_blocking", "1"),
    ("include_blocked_by", "1"),
    ("include_followed_by", "1"),
    ("include_want_retweets", "1"),
    ("include_mute_edge", "1"),
    ("include_can_dm", "1"),
    ("include_can_media_tag", "1"),
    ("include_ext_is_blue_verified", "1"),
    ("include_ext_verified_type", "1"),
    ("include_ext_profile_image_shape", "1"),
    ("skip_status", "1"),
    ("dm_secret_conversations_enabled", "false"),
    ("krs_registration_enabled", "true"),
    ("cards_platform", "Web-12"),
    ("include_cards", "1"),
    ("include_ext_alt_text", "true"),
    ("include_ext_limited_action_results", "true"),
    ("include_quote_count", "true"),
    ("include_reply_count", "1"),
    ("tweet_mode", "extended"),
    ("include_ext_views", "true"),
    ("dm_users", "false"),
    ("include_groups", "true"),
    ("include_inbox_timelines", "true"),
    ("include_ext_media_color", "true"),
    ("supports_reactions", "true"),
    ("supports_edit", "true"),
    ("include_conversation_info", "true"),
    (
        "ext",
        "mediaColor,altText,mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl,article",
    ),
)

response = requests.get(
    "https://x.com/i/api/1.1/dm/conversation/1798995068067663872-1860953157419028480.json",
    headers=headers,
    params=params,
    proxies={"http": "http://localhost:7890", "https": "http://localhost:7890"},
)

print(response.json())
# NB. Original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
# response = requests.get('https://x.com/i/api/1.1/dm/conversation/1798995068067663872-1860953157419028480.json?context=FETCH_DM_CONVERSATION&include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_is_blue_verified=1&include_ext_verified_type=1&include_ext_profile_image_shape=1&skip_status=1&dm_secret_conversations_enabled=false&krs_registration_enabled=true&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_ext_limited_action_results=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_ext_views=true&dm_users=false&include_groups=true&include_inbox_timelines=true&include_ext_media_color=true&supports_reactions=true&supports_edit=true&include_conversation_info=true&ext=mediaColor%2CaltText%2CmediaStats%2ChighlightedLabel%2CvoiceInfo%2CbirdwatchPivot%2CsuperFollowMetadata%2CunmentionInfo%2CeditControl%2Carticle', headers=headers)
