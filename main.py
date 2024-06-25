from lib.http_server import HTTPServer

HOST = "localhost"

PORT = 4221

if __name__ == "__main__":
    HTTPServer.listen(HOST,PORT)