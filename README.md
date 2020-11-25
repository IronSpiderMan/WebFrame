# 一、Web框架
首先我们今天要做的事是开发一个Web框架。可能听到这你就会想、是不是很难啊？这东西自己能写出来？

如果你有这种疑惑的话，那就继续看下去吧。相信看完今天的内容你也能写出一个自己的Web框架。

## 1.1、Web服务器

要知道什么是Web框架首先要知道Web服务器的概念。Web服务器是一个无情的收发机器，对它来说，接收和发送是最主要的工作。在我们用浏览器打开网页时，如果不考虑复杂情况，我们可以理解为我们在向服务器要东西，而服务器接到了你的请求后，根据一些判断，再给你发送一些内容。

仔细一想，其实这一个套接字（Socket）。

## 1.2 Web框架

那Web框架是什么呢？Web框架其实就是对Web服务器的一个封装，最原始的服务器只有一个原生的Socket，它可以做一些基本的工作。但是想用原生Socket做Web开发，那你的事情就多了去了。

而Web框架就是对Socket的高级封装，不同的Web框架封装程度不同。像Django是封装地比较完善的一个框架，而Flask则要轻便得多。

那他们只会封装Socket吗？我们接着往下看！

## 1.3 MVC和MTV

现在大多数框架都是MCV模式或者类MCV模式的。那MCV的含义是什么呢？具体含义如下：

1. model：模型层
2. view：视图层
3. controller：控制层（业务逻辑层）

下面我们来具体解释一下：

**模型**很好理解，就是我们常说的类，我们通常会将模型和数据库表对应起来。

**视图层**关注的是我们展示的页面效果，主要就是html、css、js等。

**控制层**，其实把它称作**业务逻辑层**要更好理解。也就是决定我要显示什么数据。

如果拿登录的业务来看。数据库中用户表对应的类就是属于模型层，我们看到的登录页面就是视图层，而我们处理判断登录的用户名密码等一系列内容就是业务逻辑层的内容。

那MTV又是什么呢？其实MTV就是MCV的另一种形式，model是一样的，而T的含义是Template，对应View。比较奇怪的就是MTV中的View，它对应Controller。

其实MVC和MTV没有本质区别。

## 1.4、框架封装的内容

在大多数框架中我们都不会去关注Socket本身，而更多的是去关注MTV三个部分。在本文，我们会去自己实现Template和View两个部分。

Template部分很好理解，就是我们通常的html页面。但是我们最终要实现的是动态页面（页面中的数据是动态生成的），因此我们需要对传统的html页面进行一些改造。这部分的工作需要我们定义一些特征标记，以及对html进行一些渲染工作。

而View部分我们会实现两个功能，一个是路由分发，另一个是视图函数。

路由分发的工作就是让我们对应不同的url，响应不同的内容。比如我请求`http://www.test.com/login.html`会返回登录页面，如果请求`http://www.test.com/register.html`则返回注册页面。

而视图函数则是针对每个请求的处理。后面我们会再提到。

知道了上面这些知识后，我们就可以着手开发我们的Web框架了。

# 二、实现一个Web服务器

服务器是Web框架的基础，而Socket是服务器的基础。因此我们还需要了解一下Socket的使用。

## 2.1 socket的使用

在python中socket的操作封装在socket.socket类中。我们先看下面这段代码，如何再来逐一解释：

```python
import socket
# 创建一个服务端socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定ip和端口
server.bind(('127.0.0.1', 8000))
# 监听是否有请求
server.listen(1)
# 接收请求
conn, addr = server.accept()
# 接收数据
data = conn.recv(1024)
print(addr)
print(data.decode('utf-8'))
```

在我们做操作前，我们需要创建一个socket对象。在创建是我们传入了两个参数，他们规定了如下内容：

1. socket.AF_INET：ipv4
2. socket.SOCK_STREAM：TCP协议

有了socket对象后，我们使用bind方法绑定ip和端口。其中127.0.0.1表示本机ip，绑定后我们就可以通过指定ip和端口访问了。

因为是服务器，所以我们需要使用listen监听是否有请求，listen方法是阻塞的，他会一直等待。

当监听到请求后，我们可以通过accept方法接收请求。accept方法会返回连接和请求的地址信息（ip和端口）。

然后通过conn.recv就可以获取客户端发来的数据了。recv方法中传入的参数是接收的最大字节数。

在网络传输过程中，数据都是二进制形式传输的，因此我们需要对数据进行解码。

我们可以编写一个client来测试一下：

```python
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 8000))
client.send("你好".encode('utf-8'))
```

我们依次运行服务端，和客户端。会发现客户端输出如下内容：

```python
('127.0.0.1', 49992)
你好
```

可以看到客户端成功将数据发送给了服务端。

## 2.2、实现Web服务器

上面只是简单看一下socket的使用，那种程度的服务器还不能满足我们网站的需求。我们来看看它有些上面问题：

1. 没有响应
2. 只能接收一个请求

关于没有响应的问题很好解决，我们只需要在服务端加下面两句代码：

```python
conn.send('你好'.encode('utf-8'))
conn.close()
```

现在我们运行服务端，客户端你已经可以删除了。因为微软已经帮我们实现了一个客户端，就是鼎鼎大名的IE浏览器。我们打开IE浏览器在url输入：`http://127.0.0.1:8000/`就可以看到如下页面：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201125184614525.png#pic_center)

可能有些人就发现了，这个其实是用utf-8编码然后用gbk解码的“你好”。这个其实就是我们编写的服务器返回的内容。

但是如果你再次访问这个页面，浏览器就会无情地告诉你“无法访问此页面”。因为我们服务端已经停止了，我们可以给我们的服务器加个while循环：

```python
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 8000))
server.listen(5)
while True:
    conn, addr = server.accept()
    data = conn.recv(1024)
    conn.send("你好".encode('gbk'))
    conn.close()
```

这样我们就可以一直访问了。但是实际上它还是有问题，因为它同一时间只能接收一个连接。想要可以同时接收多个连接，就需要使用多线程了，于是我我把服务端修改为如下：

```python
import socket
from threading import Thread


def connect(conn):
    data = conn.recv(1024)
    conn.send("你好".encode('gbk'))
    conn.close()


def run_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8000))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        t = Thread(target=connect, args=(conn, ))
        t.start()
    
    
run_server()

```

我们在accept部分不停地接收连接，然后开启一个线程给请求返回数据。这样我们就解决了一次请求服务器就会停止的问题了。为了方便使用，我用面向对象的方式重写了服务器的代码：

```python
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
        conn.send("你好".encode('gbk'))
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

```

这样我们只需要编写下面的代码就能运行我们的服务器了：

```python
import socket
from server import Server

my_server = Server('127.0.0.1', 8000, 5, socket.AF_INET, socket.SOCK_STREAM)
my_server.run()

```

现在我们的服务端写好了，我们再来关注一下Template和View部分。

# 三、模板

在上面我们的服务端只返回了一个简单的字符串，下面我们来看看如何让服务器返回一个html页面。

## 3.1 返回html页面

其实想要返回html非常简单，我们只需要先准备一个html页面，我们创建一个template模板，并在目录下创建index.html文件，内容如下：

```python
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>Do not go gentle into that good night!</h1>
</body>
</html>
```

我们只写了一个h标签，然后在Server类中的conn方法做一点简单的修改：

```python
@staticmethod
def conn(conn):
    # 获取请求参数
    request = conn.recv(1024)
    with open('template/index.html', 'rb') as f:
        conn.send(f.read())
        conn.close()
```

我们把原本发送固定字符串改成了发送从文件中读取的内容，我们再次在IE中访问`http://127.0.0.1:8000/`可以看到如下页面：

![在这里插入图片描述](https://img-blog.csdnimg.cn/2020112520030660.png#pic_center)

这样我们想要返回不同的页面只需要修改html文件就好了。但是上面的方式还不能让我们动态地显示数据，因此我们还需要继续修改。

## 3.2 模板标记

想要动态显示数据，我们肯定需要对html的内容进行二次处理。为了方便我们二次处理，我们可以定义一些特殊标记，我们把它们称作【模板标记】。比如下面这个html文件：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <h1>username: %%username%%</h1>
    <h1>password: %%password%%</h1>
</body>
</html>
```

其中`%%username%%`就是我们定义的模板标记。我们只需要在服务端找到这些标记，然后替换就好了。于是我将conn方法修改为如下：

```python
@staticmethod
def conn(conn):
    # 获取请求参数
    request = conn.recv(1024)
    html = render('template/index.html', {'username': 'zack', 'password': '123456'})
   	conn.send(html.encode('gbk'))
    conn.close()
```

这次我们不再是直接把html的内容发送出去了，而是把模板的路径交由render函数进行读取并渲染。我们来看看render函数：

```python
def render(template_path, params={}):
    with open(template_path, 'r') as f:
        html = f.read()
    # 找到所有模板标记
    if params:
        markers = re.findall('%%(.*?)%%', html)
        for marker in markers:
            tag = re.findall('%%' + marker + '%%', html)[0]
            if params.get('%s' % marker):
                html = html.replace(tag, params.get('%s' % marker))
            else:
                html = html.replace(tag, '')
    return html

```

我们的render函数接收两个参数，分别是模板路径代码，和用来渲染的参数。我们使用正则表达式找出特殊标记，然后用对应的变量进行替换。最后再把渲染后的结果返回，我们来访问一下：`http://127.0.0.0:8000/`可以看到如下页面：

![在这里插入图片描述](https://img-blog.csdnimg.cn/20201125204119368.png#pic_center)

可以看到我们渲染成功了。在我们知道如何渲染页面后，我们就可以从数据库取数据，然后再渲染到页面上了。不过这里就不再细说下去了。

# 四、路由系统和视图函数

在上面的例子中，我们都是只能返回一个页面。接下来我们就来实现一个可以根据url来返回不同页面的框架。

## 4.1 路由系统

其实路由系统就是一个url和页面的对应关系，为了方便修改，我们另外创建一个urls.py文件，内容大致如下：

```python
from views import *

urlpatterns = {
    '/index': index,
    '/login': login,
    '/register': register,
    '/error': error
}
```

在里面我们写了一个字典。而且还导入了一个views模块，这个模块我们稍后会创建。

我们来看看它的作用，首先我们需要知道，字典的值是一个个函数。知道这点后我们就能很简单地猜测到，其实这个urlpatterns就是url和函数地对应关系。下面我们来把views模块创建一下。

## 4.2 视图函数

我们的视图视图函数通常需要一个参数，就是我们的请求内容。我们可以封装成一个request类，我为了方便就直接接收字符串：

```python
import re

def render(template_path, params={}):
    with open(template_path, 'r') as f:
        html = f.read()
    # 找到所有模板标记
    if params:
        markers = re.findall('%%(.*?)%%', html)
        for marker in markers:
            tag = re.findall('%%' + marker + '%%', html)[0]
            if params.get('%s' % marker):
                html = html.replace(tag, params.get('%s' % marker))
            else:
                html = html.replace(tag, '')
    return html

def index(request):
    return render('template/index.html', {'username': 'zack', 'password': '123456'})

def login(request):
    return render('template/login.html')

def register(request):
    return render('template/register.html')

def error(request):
    return render('template/error.html')
```

我们在视图函数定义了一系列函数，这样我们就可以针对不同的url发送不同的响应了。另外我把render函数移到了views模块。

那我们要怎样才能让视图函数来处理不同的请求呢？这个时候我们就需要想一下谁是第一个拿到请求的。我想你应该也想到了，就是我们的Socket服务器，所有我们还要回到Server类。

## 4.3、请求参数

我们到现在还没有看到IE给我们服务器发的东西，现在我们来看一看：

```python
b'GET / HTTP/1.1\r\nAccept: text/html, application/xhtml+xml, image/jxr, */*\r\nAccept-Language: zh-Hans-CN,zh-Hans;q=0.5\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko\r\nAccept-Encoding: gzip, deflate\r\nHost: 127.0.0.1:8000\r\nConnection: Keep-Alive\r\n\r\n'
```

把上面的内容整理后：

```python
b'GET / HTTP/1.1
\r\n
Accept: text/html, application/xhtml+xml, image/jxr, */*
\r\n
Accept-Language: zh-Hans-CN,zh-Hans;q=0.5
\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
\r\
nAccept-Encoding: gzip, deflate
\r\n
Host: 127.0.0.1:8000
\r\n
Connection: Keep-Alive
\r\n\r\n'
```

可以看到它们都是由`\r\n`拆分的字符串，而且在第一行就有我们的请求url的信息。可能你看不出，但是经验丰富的我一眼就看出了，因为我请求的url是`http://127.0.0.1:8000/`，所以我们的请求url是/。

知道这些后，那接下来的工作就是字符串处理了。我把Server的conn函数修改为如下：

```python
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
```

我们先是通过字符串分割的方式提取出url，然后在路由系统中匹配视图函数，把请求参数传递给视图函数，视图函数就会帮我们渲染一个html页面，我们把html返回给浏览器。这样我们就实现了一个相对完整的web框架了！

当然，这个框架是不能使用到生成中的，大家可以通过这个案例来理解Web框架的各个部分。

可能有些机智的读者尝试用Chrome或者Edge浏览器访问上面的服务器，但是却被拒绝了。

因为我们的响应信息只是并没有包含响应头，Chrome认为我们响应的东西是不正规的，因此不让我们访问。大家可以尝试着自己解决一下这个问题。

今天的内容就到这里了！感兴趣的读者可以关注公众号“新建文件夹X”，感谢阅读。