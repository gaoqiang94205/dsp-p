import json

class node(object):
    @property
    def state(self):
      return self._state

    @state.setter
    def state(self,value):
      if value not in ('ready','down'):
          raise ValueError('the state value is not illegal')
      else:
          self._state = value

    @property
    def host(self):
        return self._host
    @host.setter
    def host(self,host):
        self._host = host

    @property
    def address(self):
        return self._address
    @address.setter
    def address(self, address):
        self._address = address

    @property
    def role(self):
        return self._role
    @role.setter
    def role(self,role):
      self._role = role

if __name__ == '__main__':
    n = node()
    n.state = 'ready'
    n.role = 'leader'
    n.address='asaa'
    dic = n.__dict__
    print json.dumps(dic);