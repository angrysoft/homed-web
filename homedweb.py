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

__author__ = 'Sebastian Zwierzchowski'
__copyright__ = 'Copyright 2019 Sebastian Zwierzchowski'
__license__ = 'GPL2'
__version__ = '0.1'

from starlette.applications import Starlette
from starlette.staticfiles import StaticFiles
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.templating import Jinja2Templates
import logging
from pycouchdb import Server
import operator
import uvicorn
import json
import os

conf_file = 'homedweb.json'
if not os.path.exists(conf_file):
    raise FileNotFoundError('can`find config file /etc/homerelay.json')

config ={}
with open(conf_file) as jfile:
    config = json.load(jfile)

db = Server(user=config['db']['user'], password=config['db']['password'])


templates = Jinja2Templates(directory='templates')

app = Starlette(debug=True)
app.mount('/static', StaticFiles(directory='static'), name='static')

logging.basicConfig(filename='gast.log', filemode='w', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
logging.warning('app starts')


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'userid' not in session:
            return redirect(url_for('login', next=request.url))
        return func(*args, **kwargs)
    return decorated_function


@app.route('/{homeid:str}')
# @login_required
async def devices(request) -> PlainTextResponse:
    homeid: str = request.path_params['homeid']
    if homeid == 'favicon.ico':
        return PlainTextResponse(homeid)
    places = dict()
    # items_list = sorted([d for d in db[homeid]], key=operator.itemgetter('name'))
    
    for item in db[homeid].get_all_docs():
        place: str = item.get('place', '')
        print(place)
        if not place:
            continue
        if place not in places:
            places[place] = list()
        places[place].append(item)
    print(places)
    return templates.TemplateResponse('devices.html', {"request": request, "places": places})


if __name__ == "__main__":
    uvicorn.run(app, host='127.0.0.1',debug=True, port=8000)
