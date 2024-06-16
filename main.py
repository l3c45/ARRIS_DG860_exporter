import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import re
from requests import Session
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger('main')

ARRIS_URL = "http://192.168.100.1/cgi-bin/status_cgi"

def generate_metrics(result_body, tds, index):
    metric_template = "arris_downstream_{metric}{{index=\"{index}\",modulation=\"{modulation}\",channel_id=\"{channel}\",frequency=\"{freq}\"}} {value}"
    fields = [
        ("packets_corrected", 7),
        ("packets_uncorrectable", 8),
        ("power", 3),
        ("snr", 4),
    ]
    common_data = {
        "index": index,
        "modulation": tds[5].get_text(),
        "channel": tds[1].get_text(),
        "freq": tds[2].get_text().split(' ')[0]
    }
    for metric, idx in fields:
        result_body.append(metric_template.format(metric=metric, value=tds[idx].get_text().strip().split(' ')[0], **common_data))

def process():
    result_body = []
    try:
        response = Session().get(ARRIS_URL)
        response.raise_for_status()
    except Exception as e:
        log.error(f"Exception: {e}")
        return ''

    soup = BeautifulSoup(re.sub(r'(\r|\n|\t)', '', response.text), 'html.parser')
    downstream_table = soup.find_all('table')[1]

    for index, tr in enumerate(downstream_table.find_all('tr')[1:], start=1):
        generate_metrics(result_body, tr.find_all('td'), index)

    return '\n'.join(result_body)

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.respond()

    def handle_http(self, status, body):
        self.send_response(status)
        self.send_header('Content-type', 'text/plain;charset=UTF-8')
        self.end_headers()
        return body.encode('utf-8')

    def respond(self):
        content = self.handle_http(200, process())
        try:
            self.wfile.write(content)
        except Exception as e:
            log.error(f"Exception when trying to write to socket: {e}")

def main():
    server_address = ('0.0.0.0', 9393)
    httpd = HTTPServer(server_address, Server)
    log.info("Starting http server.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

if __name__ == '__main__':
    main()
