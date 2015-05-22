import pkgutil
import redis
from redis.connection import ConnectionError

class Limit():

    def __init__(self, host='localhost', port=6379, root='rate-limit'):
        self._redis = redis.Redis(host=host, port=port)
        self._root = root
        self._lua = self._getLua()

    def checkRate(self, name, max, duration):
        """
        Query for rate

        :param name:
        :param max:
        :param duration:
        :return: <LIMITRESULT>
        """
        self.assertRedis()

        ok, count, reset = self._lua(
            keys=['rate_limit:' + name],
            args=[
                max,
                duration
            ])
        return LimitResult(name, bool(ok), int(count), duration, int(reset))


    def _getLua(self):
        """
        Registers LUA script in redis.  If it fails then we silently proceed

        :return:
        """
        result = None
        try:
            data = pkgutil.get_data('rate_limit', 'lua/over_limit.lua')
            result = self._redis.register_script(data)
        except ConnectionError:
            pass
        finally:
            return result


    def assertRedis(self):
        """
        Validate redis is available
        """
        if self._lua is None:
            raise RedisUnavailable()


class LimitResult():
    """
    Result class for checkRate results
    """
    def __init__(self, name, ok, count, duration, reset):
        self.name = name
        self.ok = ok
        self.count = count
        self.duration = duration
        self.reset = reset


class RedisUnavailable(Exception):
    pass