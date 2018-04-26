import logging
import uuid

import etcd

_log = logging.getLogger(__name__)

DEFAULT_TTL = 30
DEFAULT_TIMEOUT = 5


class EtcdLock(object):
    def __init__(self, client, lock_key, token=None, ttl=DEFAULT_TTL):
        self.client = client
        self.lock_key = lock_key
        self.ttl = ttl
        self._token = token or uuid.uuid4().hex

        _log.debug("Initializing lock for %s with token %s", self.lock_key, self._token)

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        raise ValueError("Can't modify token value.")

    def acquire(self):
        prev_lock = self.get_lock()
        if not prev_lock:
            _log.debug("Prev Lock not found.")
            # not locked yet
            try:
                _log.debug("Try to lock.")
                self.client.write(self.lock_key, self.token, ttl=self.ttl, prevExist=False)
            except etcd.EtcdAlreadyExist:
                # some candidate locked
                _log.debug("Other candidate locked.")
                return False
            else:
                # successfully get the lock
                _log.debug("Lock succeed.")
                return True
        else:
            # already has been locked by self or others, have to check token
            return self._is_acquired()

    def refresh(self):
        prev_lock = self.get_lock()
        is_succeed = False
        if prev_lock:
            try:
                prev_lock.ttl = self.ttl
                self.client.update(prev_lock)
            except etcd.EtcdException as e:
                _log.error("Refresh lock failed: %s.", str(e))
            except Exception as e:
                _log.error("Refresh lock failed: Unexpected error %s.", str(e))
            else:
                is_succeed = True
        else:
            _log.error("Refresh lock failed, lock not found.")

        return is_succeed

    def get_lock(self):
        try:
            result = self.client.read(self.lock_key)
            return result
        except etcd.EtcdKeyNotFound:
            return None

    def _is_acquired(self):
        prev_lock = self.get_lock()
        return bool(prev_lock and prev_lock.value == self.token)
