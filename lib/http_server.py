import socket
from lib.HTTP_header_names import HTTPHeaderNames
from lib.http_responses import HttpResponse
from lib.http_requests import HTTPRequests
from lib.http_status_codes import HttpStatusCode

class HTTPServer:
    MAX_REQUEST_SIZE = 1024
    ENCODING =  "utf-8"

    @classmethod
    def listen(cls,host,port):
        with socket.create_server((host,port),reuse_port=True) as server_socket:
            print(f'Listening on {host}:{port}')
            while True:
                client_socket, _ = server_socket.accept()
                with client_socket:
                    cls._handle_client(client_socket)

    @classmethod
    def _handle_client(cls, socket):
        try:
            data = socket.recv(cls.MAX_REQUEST_SIZE).decode(cls.ENCODING)
            if not data:
                return
            request = HTTPRequests(data)
            response = cls._handle_request(request)
            socket.sendall(str(response).encode(HTTPServer.ENCODING))
        except Exception as e:
            print(f'Error handling request {e}')
    
    @classmethod
    def _handle_request(cls,request):
        url_segments = request.request_target.split('/')
        
        if request.http_method =='GET':
            if request.request_target == '/':
                return HttpResponse(HttpStatusCode.OK)
            elif url_segments[1] == 'echo' and len(url_segments) >2:
                response =  HttpResponse(HttpStatusCode.OK)
                response.write_body(url_segments[2])
                return response
            elif url_segments[1] == 'user-agent':
                response = HttpResponse(HttpStatusCode.OK)
                user_agent = request.headers.get(HTTPHeaderNames.USER_AGENT)
                if user_agent:
                    response.write_body(user_agent)
                return response
            
        return HttpResponse(HttpStatusCode.NOT_FOUND)
            
