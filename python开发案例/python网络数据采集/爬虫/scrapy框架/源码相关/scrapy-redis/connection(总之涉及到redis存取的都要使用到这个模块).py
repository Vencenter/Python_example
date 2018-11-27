# coding = utf-8

'''
@author = super_fazai
@File    : connection(总之涉及到redis存取的都要使用到这个模块).py
@Time    : 2017/9/5 21:47
@connect : superonesfazai@gmail.com
'''

"""
负责根据setting中配置实例化redis连接。
被dupefilter和scheduler调用，总之涉及到redis存取的都要使用到这个模块
"""

# 这里引入了redis模块，这个是redis-python库的接口，用于通过python访问redis数据库，
# 这个文件主要是实现连接redis数据库的功能，这些连接接口在其他文件中经常被用到

import redis
import six

from scrapy.utils.misc import load_object

DEFAULT_REDIS_CLS = redis.StrictRedis

# 可以在settings文件中配置套接字的超时时间、等待时间等
# Sane connection defaults.
DEFAULT_PARAMS = {
    'socket_timeout': 30,
    'socket_connect_timeout': 30,
    'retry_on_timeout': True,
}

# 要想连接到redis数据库，和其他数据库差不多，需要一个ip地址、端口号、用户名密码（可选）和一个整形的数据库编号
# Shortcut maps 'setting name' -> 'parmater name'.
SETTINGS_PARAMS_MAP = {
    'REDIS_URL': 'url',
    'REDIS_HOST': 'host',
    'REDIS_PORT': 'port',
}


def get_redis_from_settings(settings):
    """Returns a redis client instance from given Scrapy settings object.
    This function uses ``get_client`` to instantiate the client and uses
    ``DEFAULT_PARAMS`` global as defaults values for the parameters. You can
    override them using the ``REDIS_PARAMS`` setting.
    Parameters
    ----------
    settings : Settings
        A scrapy settings object. See the supported settings below.
    Returns
    -------
    server
        Redis client instance.
    Other Parameters
    ----------------
    REDIS_URL : str, optional
        Server connection URL.
    REDIS_HOST : str, optional
        Server host.
    REDIS_PORT : str, optional
        Server port.
    REDIS_PARAMS : dict, optional
        Additional client parameters.
    """
    params = DEFAULT_PARAMS.copy()
    params.update(settings.getdict('REDIS_PARAMS'))
    # XXX: Deprecate REDIS_* settings.
    for source, dest in SETTINGS_PARAMS_MAP.items():
        val = settings.get(source)
        if val:
            params[dest] = val

    # Allow ``redis_cls`` to be a path to a class.
    if isinstance(params.get('redis_cls'), six.string_types):
        params['redis_cls'] = load_object(params['redis_cls'])

    # 返回的是redis库的Redis对象，可以直接用来进行数据操作的对象
    return get_redis(**params)


# Backwards compatible alias.
from_settings = get_redis_from_settings


def get_redis(**kwargs):
    """Returns a redis client instance.
    Parameters
    ----------
    redis_cls : class, optional
        Defaults to ``redis.StrictRedis``.
    url : str, optional
        If given, ``redis_cls.from_url`` is used to instantiate the class.
    **kwargs
        Extra parameters to be passed to the ``redis_cls`` class.
    Returns
    -------
    server
        Redis client instance.
    """
    redis_cls = kwargs.pop('redis_cls', DEFAULT_REDIS_CLS)
    url = kwargs.pop('url', None)

    if url:
        return redis_cls.from_url(url, **kwargs)
    else:
        return redis_cls(**kwargs)