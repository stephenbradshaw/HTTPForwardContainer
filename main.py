from flask import Flask, request, Response
import requests
import os
import urllib3

# allows for debugging
DEBUG=bool(os.getenv('DEBUG', False))
SCHEME=os.getenv('SCHEME','http')
TESTROUTE=os.getenv('TESTROUTE', 'b8af860c6c7f78d5cbcaa86c8f11b268cd0c0295') 

app = Flask(__name__)


@app.route(f'/{TESTROUTE}')
def health():
    return "OK"


@app.route('/', defaults={'url': ''}, methods=["GET", "POST", "PUT"])
@app.route('/<path:url>', methods=["GET", "POST", "PUT"])
def root(url):
    host=os.getenv('DESTINATION')
    timeout = int(os.getenv('TIMEOUT', 20)) # override using TIMEOUT env variable
    scheme = SCHEME
    path = f'{scheme}://{host}/{url}'
    try:
        headers = dict(request.headers)
        if not 'accept-encoding' in [a.lower() for a in headers.keys()]:
            headers['Accept-Encoding'] = urllib3.util.SKIP_HEADER # stop requests from adding this header
        r = requests.request(request.method, path, params=request.args, stream=True, 
                            headers=headers, allow_redirects=False, 
                            data=request.get_data(), timeout=timeout)
        def generate():
            for chunk in r.raw.stream(decode_content=False):
                yield chunk


        out = Response(generate(), headers=dict(r.raw.headers))
        out.status_code = r.status_code
        return out
    except Exception as e:
        # change these responses to remove indicators
        if DEBUG:
            return f'Error: {str(e)}'
        else:
            return 'Error'
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 80)))