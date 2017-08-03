import BaseHTTPServer
import sys, os, BaseHTTPServer

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    Page = '''
    <html>
    <body>
        <table>
        <tr> 
            <td>Header</td>
            <td>Vaule</td>
        </tr>
        <tr>
            <td>Data and time</td>
            <td>{date_time}</td>
        </tr>
        <tr>
            <td>Client host</td>
            <td>{client_host}</td>
        </tr>
        <tr>
            <td>Command</td>
            <td>{command}</td>
        </tr>
        <tr>
            <td>Path</td>
            <td>{path}</td>
        </tr>
        </table>
    </body>
    </html>
 
    '''

    Error_Page = """\
        <html>
        <body>
        <h1>Error accesing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """
    
    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg = msg)
        self.send_content(content)
     

    def do_GET(self):
        try:
            full_path = os.getcwd() + self.path
            if not os.path.exists(full_path):
                raise ServerException("'{0}' not found".format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise ServerException("Unknown object '{0}'".format(self.path))
        except Exception as msg:
            self.handle_error(msg)
 
    def create_page(self):
        values = {
            'date_time' : self.date_time_string(),
            'client_host' : self.client_address[0],
            'client_port' : self.client_address[1],
            'command' : self.command,
            'path' : self.path
        }
        page = self.Page.format(**values)
        return page        

    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)

class ServerException(Exception):
    ''' internal error '''
    pass

if __name__ == '__main__':
    serverAddress = ('', 8080)
    server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
    server.serve_forever()
