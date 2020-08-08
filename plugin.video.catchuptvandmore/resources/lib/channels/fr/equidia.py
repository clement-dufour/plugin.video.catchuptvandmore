# -*- coding: utf-8 -*-
"""
    Catch-up TV & More
    Copyright (C) 2019  SylvainCecchetto

    This file is part of Catch-up TV & More.

    Catch-up TV & More is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    Catch-up TV & More is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with Catch-up TV & More; if not, write to the Free Software Foundation,
    Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

# The unicode_literals import only has
# an effect on Python 2.
# It makes string literals as unicode like in Python 3
from __future__ import unicode_literals
from datetime import date

from codequick import Route, Resolver, Listitem, utils, Script

from resources.lib import web_utils
from resources.lib.menu_utils import item_post_treatment

import json
import urlquick

# TODO
# Add Replay

URL_API = "https://equidia-vodce-players.hexaglobe.net"

URL_LIVE_DATAS = URL_API + '/mf_data/%s.json'


@Resolver.register
def get_live_url(plugin, item_id, **kwargs):

    # Get date of Today
    today = date.today()
    today_value = today.strftime("%Y%m%d")
    resp = urlquick.get(
        URL_LIVE_DATAS % today_value, headers={"User-Agent": web_utils.get_random_ua()}, max_age=-1)
    json_parser = json.loads(resp.text)
    url_stream_datas = ''
    for stream_datas in json_parser:
        if 'EQUIDIA' in stream_datas['title']:
            url_stream_datas = stream_datas["streamUrl"]
    resp2 = urlquick.get(
        url_stream_datas, headers={"User-Agent": web_utils.get_random_ua()}, max_age=-1)
    json_parser2 = json.loads(resp2.text)
    return json_parser2["primary"]