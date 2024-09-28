import json
import os
from werkzeug.wrappers import Response

class TokenMiddleware:
    
    exclude_routes = {'/ai/interaction-recommendations', 
                      '/ai/category-recommendations'}
    
    def __init__(self, app, exclude_routes = None):
        self.app = app
        if exclude_routes:
            self.exclude_routes.update(exclude_routes)

    def __call__(self, environ, start_response):
        # Get the request method and path
        request_method = environ.get('REQUEST_METHOD')
        path_info = environ.get('PATH_INFO')

        # Skip middleware for static files or specific paths if necessary
        if path_info.startswith('/static') or path_info in self.exclude_routes:
            return self.app(environ, start_response)

        # Check for token in the CLIENT_HEADER_SECRET
        token = environ.get('HTTP_CLIENT_HEADER_SECRET')

        if not token:
            return self._unauthorized(start_response, 'Token is missing!')

        if not self.is_valid_token(token):
            return self._unauthorized(start_response, 'Invalid token!')

        return self.app(environ, start_response)

    def _unauthorized(self, start_response, message):
        # Build a raw WSGI response
        response_body = json.dumps({'error': message})
        status = '401 UNAUTHORIZED'
        headers = [('Content-Type', 'application/json')]

        # Start the response
        start_response(status, headers)

        # Return the response body
        return [response_body.encode('utf-8')]

    def is_valid_token(self, token):
        # Validate the token against the environment variable
        return token == os.environ.get('CLIENT_HEADER_SECRET')
