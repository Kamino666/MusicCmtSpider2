from threading import Thread
import requests


class WebStream(Thread):
    proxies = {'https': 'http://14.20.235.169:30862', 'http': 'http://116.196.87.86:20183'}

    # proxies = {'http': '113.121.39.150:9999'}

    def __init__(self, webQueue, parseQueue):
        Thread.__init__(self)
        self.webQueue = webQueue
        self.parseQueue = parseQueue

    def run(self):
        """
        开始执行任务
        :return: 
        """
        count = 0
        while True:
            if self.webQueue.empty():  # debug 假如队列空了就不干了
                break
            task = self.webQueue.get()  # 获取任务
            # debug 测试requests模块
            text = self.getHtmlText(task[0], task[1])
            # print(text)
            # debug 测试解析模块
            if count == 0:
                self.parseQueue.put((text, 'toplist'))
            elif count == 1:
                self.parseQueue.put((text, 'playlist'))
            elif count == 2:
                self.parseQueue.put((text, 'hot comments'))
            count += 1

    def getHtmlText(self, url, params):
        global r
        hd = {
            'Referer': 'http://music.163.com/',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          r'Chrome/63.0.3239.132 Safari/537.36 '
        }
        try:
            # print("请求中")
            r = requests.get(url, params=params, timeout=30, headers=hd)  # proxies=self.proxies
            # print(r.headers)
            # print(r.status_code)
            r.raise_for_status()
            # print(r.apparent_encoding)
            if r.apparent_encoding == "Windows-1254":  # 不知道为什么网易云json返回的编码是这玩意
                r.encoding = 'utf-8'
            else:
                r.encoding = r.apparent_encoding
            return r.text
        except requests.HTTPError:
            return "连接异常："
        except requests.ConnectionError:
            return "连接错误"
        except requests.Timeout:
            return "连接超时"
        except Exception as e:
            return "未知错误" + str(e)
        finally:
            print(r.status_code)
