# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 Alexander Shorin
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#

from astm import codec
from astm import constants
from astm.exceptions import NotAccepted
from astm.client import Client

class emitter(object):

    def __init__(self, *args):
        self.outbox = list(args)
        self.pos = 0
        self.inbox = []

    def __iter__(self):
        return self

    def next(self):
        if self.pos >= len(self.outbox):
            raise StopIteration
        item = self.outbox[self.pos]
        self.pos += 1
        return item

    __next__ = next

    def send(self, value):
        self.inbox.append(value)
        return self.next()

    def put(self, record):
        self.outbox.append(record)


def messages_workflow():
    def emitter():
        yield ['H']
        yield ['C']
        yield ['P']
        yield ['O']
        yield ['O']
        yield ['P']
        yield ['C']
        yield ['O']
        yield ['O']
        yield ['C']
        yield ['R']
        yield ['C']
        yield ['R']
        yield ['R']
        yield ['L']
    client = Client(emitter, host='127.0.0.1', port=15200)
    client.handle_connect()
    client.on_ack()
    while client.outbox[-1] is not None:
        client.on_ack()


def chunked_response():
    def emitter():
        assert (yield ['H', 'foo', 'bar'])
        assert (yield ['L', 'bar', 'baz'])
    client = Client(emitter, chunk_size=12, host='127.0.0.1', port=15200)
    client.handle_connect()
    while client.outbox[-1] is not None:
        client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()


def bulk_mode():
    def emitter():
        assert (yield ['H', 'foo', 'bar'])
        assert (yield ['L', 'bar', 'baz'])
    client = Client(emitter, chunk_size=12, host='127.0.0.1', port=15200)
    client.handle_connect()
    while client.outbox[-1] is not None:
        client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()
    #client.on_ack()


if __name__ == '__main__':
    messages_workflow()
    chunked_response()
    bulk_mode()
