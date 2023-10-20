# Exampe server from author at https://github.com/kxepal/python-astm/issues/1

import logging
from astm.asynclib import loop
from astm.server import Server, BaseRecordsDispatcher

# global astm logging channel configuration
log_root = logging.getLogger('astm')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s'
))
log_root.addHandler(handler)
log_root.setLevel(logging.DEBUG)

# special logging configuration for server connection handler
log_conn = logging.getLogger('astm.server.conn')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] [%(name)s] [%(levelname)s] [%(host)s:%(port)s] %(message)s'
))
log_conn.addHandler(handler)
log_conn.setLevel(logging.DEBUG)
log_conn.propagate = False


class RecordsDispatcher(BaseRecordsDispatcher):

    log = logging.getLogger('astm.server.dispatcher')

    def on_header(self, record):
        self.log.info('Header: %r', record)

    def on_patient(self, record):
        self.log.info('Patient: %r', record)

    def on_order(self, record):
        self.log.info('Order: %r', record)

    def on_result(self, record):
        self.log.info('Result: %r', record)

    def on_comment(self, record):
        self.log.info('Comment: %r', record)

    def on_unknown(self, record):
        self.log.warn('Unknown record: %r', record)

    def on_terminator(self, record):
        self.log.info('Terminator: %r', record)


if __name__ == '__main__':
    server = Server('localhost', 15200, dispatcher=RecordsDispatcher, timeout=10)
    loop(timeout=1)
