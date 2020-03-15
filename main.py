from Spider.NeteaseMusic import NeteaseMusic
from Spider.NeteaseMusic import NeteaseMusicStream
from db.MySQL import CmtsDB
from web.web import WebStream
from queue import Queue
import threading


def main():
    # url = r"http://music.163.com/discover/toplist?id=19723756"  # 获取热门榜单的url 正常
    # ?order=hot&cat=全部&limit=35&offset=0 可选参数
    # order是顺序 cat是分类 limit最大是35 offset是偏移量
    url = r"http://music.163.com/discover/playlist"  # 获取热门歌曲的url
    # 其他url大同小异
    # NEspider = NeteaseMusic(dbQueue)
    # NEspider.getMusicCmts_api(435166266, 20)
    # db = CmtsDB('localhost','root','root','musiccomments_test1')
    # db.pushsingle('test1',('real project','me',666,666,666))
    web_tasks = [('https://music.163.com/discover/toplist',{'id':'19723756'},'html'),
                 ('https://music.163.com/playlist',{'id':'2878716744'},'html'),
                 ('http://music.163.com/api/v1/resource/comments/R_SO_4_435278010',{'limit':'20','offset':'0'},'html'),]
    for task in web_tasks:  # 加入任务
        webQueue.put(task)
    ws = WebStream(webQueue, parseQueue)
    nms = NeteaseMusicStream(dbQueue,parseQueue)
    ws.setDaemon(True)
    nms.setDaemon(True)
    nms.start()
    ws.start()
    nms.join()
    ws.join()
    print("结束")


if __name__ == "__main__":
    # 网络访问队列 内容是(url,{url参数},结果类型)
    # html json
    webQueue = Queue()
    # 数据库访问队列 内容是字段元组
    # content username userid time likes
    dbQueue = Queue()
    # 解析队列 内容是(访问内容,解析类型)
    parseQueue = Queue()
    main()
