from brewapp import app
from brewapp.base.actor import ActorBase
from brewapp.base.model import *
import socket
import select
import json

class PiLightSwitcher(ActorBase):
    def recvAll(self):
        buf = ''
        self.epoll.poll(timeout=10)
        while self.epoll.poll(timeout=0.25):
            buf += self.sock.recv(512)
        # TODO: ugly hack around version-reply
        if '}\n\n{' in buf:
            buf = buf.split('\n\n')[0]
        reply = json.loads(buf)
        return reply

    def init(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            hostPortStr = app.brewapp_config['SW_PILIGHT_HOST_PORT']
            if not hostPortStr or not ':' in hostPortStr or not hostPortStr.split(':')[1].isdigit():
                app.logger.warn("SW_PILIGHT_HOST_PORT invalid, using 127.0.0.1:5005")
                host, port = ("127.0.0.1", 5005)
            host, port = (hostPortStr.split(':')[0], int(hostPortStr.split(':')[1]))
            self.sock.connect((host, port))
            self.epoll = select.epoll()
            self.epoll.register(self.sock.fileno(), select.EPOLLIN)
            self.sock.setblocking(0)
            self.sock.sendall(json.dumps({'action':'identify'}).encode())
            reply = self.recvAll()
            if not reply['status'] == 'success':
                app.logger.warn("PiLight doesn't like us: %s", reply)
                self.state = False
            return
        except Exception as e:
            app.logger.warn("Could not intialize pilight: %s", e)
            self.state = False
        self.state = True


    def cleanup(self):
        try:
            self.epoll.unregister(self.sock.fileno())
        except:
            pass
        try:
            self.sock.close()
        except:
            pass

    def getDevices(self):
        try:
            self.sock.sendall(json.dumps({'action':'request values'}).encode())
            reply = self.recvAll()
        except Exception as e:
            app.logger.warn("Could not get devices: %s", e)
            return []

        if not reply['message'] == 'values':
            app.logger.warn("Unexpected answer from PiLight: %s", reply)
            return []

        devices = []
        for val in reply['values']:
            if 'devices' in val:
                devices += val['devices']

        return devices

    def translateDeviceName(self, name):
        return name

    def switch(self, device, state='off'):
        try:
            deviceName = self.getDevices()[int(device)-1]
            app.logger.info("found device %s for id %s", deviceName, device)
            self.sock.sendall(json.dumps({'action':'control','code':{'device':deviceName, 'state':state}}).encode())
            reply = self.recvAll()
        except Exception as e:
            app.logger.warn("Could not switch device %s to %s: %s", device, state, e)
            return
        if not 'status' in reply.keys() or reply['status'] != 'success':
            self.logger.warn("Could not switch %s %s: %s", deviceName, state, reply)


    def switchON(self, device):
        self.switch(device, state='on')

    def switchOFF(self, device):
        self.switch(device, state='off')
