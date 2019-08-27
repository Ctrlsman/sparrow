import urllib
import datetime
from config import httpconfig


class Cookie:

    """
    用于cookie处理
    """

    def __init__(self):
        self.COOKIE = {}

    def set_cookie(self, key, value, expires, path, domain):
        """
        设置cookie
        """

        value = urllib.quote(value)
        self.COOKIE[key] = '='.join([key, value]) + ';'

        if expires:
            expires = (datetime.datetime.utcnow() + datetime.timedelta(seconds=expires))
            self.COOKIE[key] += ' expires=%s;' % expires.strftime('%a, %d %b %Y %H:%M:%S UTC')
        if path:
            self.COOKIE[key] += ' path=%s;' % path
        if domain:
            self.COOKIE[key] += ' domain=%s;' % domain

    def get_set_cookie_meta(self):
        if self.COOKIE:
            set_cookie = ['Set-Cookie: ' + i for i in self.COOKIE.values()]
            set_cookie_string = '\r\n'.join(set_cookie)
            return set_cookie_string
        else:
            return None


class HttpResponse:

    """
    对http请求的响应对象
    """

    STATUS = {
        200: '200 OK',
        204: '204 No Content',
        206: '206 Partial Content',
        301: '301 Moved Permanently',
        302: '302 Found',
        303: '303 See Other',
        304: '304 Not Modified',
        307: '307 Temporary Redirect',
        400: '400 Bad Request',
        401: '401 Unauthorized',
        403: '403 Forbidden',
        404: '404 Not Found',
        500: '500 Internal Server Error',
        503: '503 Service Unavailable',
    }


    def __init__(self):
        self.http_version = 'HTTP/1.1'
        self.status = self.STATUS[200]
        self.header = ''
        self.body = ''
        self.META = {
            'SERVER': httpconfig.get('__version__', 'http/1.1'),
            'CONNECTION': 'close',  # 默认关闭长连接
        }
        self.cookie = Cookie()

    def set_header(self, key, value):
        """
        :type key: str
        :type value: str
        """
        self.META[key.upper()] = value

    def set_cookie(self, key, value, expires=None, path=None, domain=None):
        self.cookie.set_cookie(key, value, expires, path, domain)

    def set_status(self, status_code):
        """ 通过状态码设定响应状态 """
        self.status = self.STATUS[status_code]

    def set_body(self, content):
        """ 设置响应正文 """
        self.body = content

    def make_header(self):
        """ 生成响应首部 """
        headers = [key + ': ' + value for key, value in self.META.items()]
        set_cookie = self.cookie.get_set_cookie_meta()
        if set_cookie:
            headers.append(set_cookie)
        self.header = '\r\n'.join(headers)

    def get_response(self):
        """ 该方法返回一个字符串形式的http响应 """
        self.make_header()
        response_line = ' '.join([self.http_version, self.status])
        response = response_line + '\r\n' + self.header + '\r\n\r\n' + self.body
        return bytes(response, encoding='utf8')


class HttpNotFound(HttpResponse):
    """
    404时的错误提示
    """
    def __init__(self):
        super(HttpNotFound, self).__init__()
        self.set_body('404 Not Found')