from werkzeug.wrappers import Request, Response

def root(environ, start_response):
    request = Request(environ)
    response = Response(f"Hello {request.args.get('name', 'World!')}!")
    return response(environ, start_response)
