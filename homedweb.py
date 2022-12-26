#!/usr/bin/python
# Copyright (C) 2019-2021 Sebastian Zwierzchowski <sebastian.zwierzchowski@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from __future__ import annotations
from threading import Thread

__author__ = "Sebastian Zwierzchowski"
__copyright__ = "Copyright 2019 - 2021 Sebastian Zwierzchowski"
__license__ = "GPL2"
__version__ = "0.1"

import json
import os
import logging
import uvicorn
from os import urandom
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import (
    JSONResponse,
    PlainTextResponse,
    RedirectResponse,
    Response,
)
from starlette.templating import Jinja2Templates
from starlette.responses import Response
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from sse_starlette.sse import EventSourceResponse
from pycouchdb import Client
from auth import AuthBackend, GoogleSignIn
from devices import HomeManager
from typing import Dict, Any, List
from functools import wraps
import asyncio


def login_required(func: Any) -> Any:
    @wraps(func)
    async def decorated_function(request: Request) -> Response:
        if request.user.is_authenticated:
            return await func(request)
        return RedirectResponse(url=f"/signin?next={request.url.path}")

    return decorated_function


@login_required
async def home(request: Request) -> Response:
    homeid: str = request.session["homeid"]
    if homeid == "favicon.ico":
        return PlainTextResponse(homeid)

    return templates.TemplateResponse("home.html", {"request": request})


@login_required
async def get_all_devices(request: Request) -> Response:
    ret: List[Dict[str, Any]] = []
    for item in db[request.session["homeid"]].get_all_docs():
        ret.append(item)
    return JSONResponse(ret)


@login_required
async def send_command(request: Request):
    cmd: bytes = await request.body()
    dm.publish_msg(cmd.decode(), request.session["homeid"])
    return PlainTextResponse("ok")


async def signin(request: Request):
    if request.method == "GET":
        return templates.TemplateResponse("signin.html", {"request": request})
    elif request.method == "POST":
        if request.user.is_authenticated:
            return PlainTextResponse("ok")

        token: bytes = await request.body()
        gs = GoogleSignIn(token.decode())
        await gs.authenticate()
        if gs.user_id in db["residents"]:
            request.session["userid"] = gs.user_id
            request.session["locale"] = gs.locale
            request.session["picture"] = gs.picture
            request.session["name"] = gs.name
            request.session["homeid"] = db["residents"][gs.user_id]["homeid"]

            return PlainTextResponse("ok")
        return PlainTextResponse("Unknown User")


@login_required
async def sse(request: Request):
    homeid: str = request.session["homeid"]

    async def messages(homeid: str):
        while True:
            print("request", await request.is_disconnected())
            # disconnected: bool = await request.is_disconnected()
            # dm.set_block_state_msg_queue(homeid, disconnected)
            # if disconnected:
            #     break
            yield {"data": "wtf"}
            
            ret = dm.get_msg_from_queue(homeid)
            if ret:
                yield {"data": ret}
            else:
                await asyncio.sleep(0.5)

    return EventSourceResponse(messages(homeid))


conf_file = os.environ.get("CONF_FILE", "/etc/homedaemon/homemanager.json")

if not os.path.exists(conf_file):
    raise FileNotFoundError(f"can`find config file {conf_file}")

config: Dict[str, Any] = {}
with open(conf_file) as jfile:
    config = json.load(jfile)

db: Client = Client(
    f"http://{config['couchdb']['user']}:{config['couchdb']['password']}@localhost"
)
dm = HomeManager(config)
dm_worker = Thread(target=dm.run, name="DeicesMSG")
dm_worker.setDaemon(True)
dm_worker.start()
templates = Jinja2Templates(directory="templates")


logging.basicConfig(
    filename="gast.log",
    filemode="w",
    format="%(asctime)s %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
)
logging.warning("app starts")


routes: List[Any] = [
    Route("/", endpoint=home),
    Route("/events", endpoint=sse),
    Route("/devices/all", endpoint=get_all_devices),
    Route("/devices/send", endpoint=send_command, methods=["POST"]),
    Route("/signin", endpoint=signin, methods=["GET", "POST"]),
]

if config.get("debug", False):
    middleware = [
        Middleware(SessionMiddleware, secret_key=str(urandom(24))),
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
    ]
else:
    middleware = [
        Middleware(SessionMiddleware, secret_key=str(urandom(24)), https_only=True),
        Middleware(AuthenticationMiddleware, backend=AuthBackend()),
    ]

app = Starlette(
    routes=routes,
    debug=True,
    middleware=middleware,
)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", debug=True, port=8000)
    print("uvicorn stop")
