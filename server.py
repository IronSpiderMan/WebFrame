import re
import urls
import socket
from threading import Thread


class Server(socket.socket):
    """
    定义服务器的类
    """

    def __init__(self, ip, host, connect_num, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self.ip = ip
        self.host = host
        self.connect_num = connect_num

    @staticmethod
    def conn(conn):
        # 获取请求参数
        request = conn.recv(1024)
        # 在request中提取method和url
        method, url, _ = request.decode('gbk').split('\r\n')[0].split(' ')
        # 在路由系统中找到对应的视图函数，并把请求参数传递过去
        html = urls.urlpatterns.get(url)(request)
        conn.send(html.encode('gbk'))
        conn.close()

    def run(self):
        """
        运行服务器
        :return:
        """
        # 绑定ip和端口
        self.bind((self.ip, self.host))
        self.listen(self.connect_num)
        while True:
            conn, addr = self.accept()
            t = Thread(target=Server.conn, args=(conn,))
            t.start()
