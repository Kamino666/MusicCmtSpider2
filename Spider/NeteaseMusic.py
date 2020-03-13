import requests
from bs4 import BeautifulSoup
import ujson
import codecs


def writeFile(data, path):
    # data.encode('utf-8').decode('gbk', 'ignore').encode('utf-8', 'ignore')
    with codecs.open(path, 'w', encoding='utf-8') as f:
        f.write(data)
    f.close()
    return f


class NeteaseMusic:

    def __init__(self):
        pass

    def getHtmlText(self, url):
        global r
        hd = {
            'Referer': 'http://music.163.com/',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          r'Chrome/63.0.3239.132 Safari/537.36 '
        }
        try:
            r = requests.get(url, timeout=30, headers=hd)
            print(r.status_code)
            r.raise_for_status()
            r.encoding = "UTF-8"
            return r.text
        except requests.HTTPError:
            return "连接异常：" + r.status_code
        except requests.ConnectionError:
            return "连接错误"
        except requests.Timeout:
            return "连接超时"
        except Exception as e:
            return "未知错误" + str(e)

    def getToplist(self, toplist_id=1):
        """
        获取并解析榜单
        1:云音乐飙升榜 2:新歌榜 3:网易原创歌曲榜 4:热歌榜
        5:说唱榜 6:古典音乐榜 7:电音榜 8:抖音榜 9:新声榜
        10:云音乐ACG音乐榜 11:韩语榜 12:国电榜 13:英语Q杂志中文周榜
        14:电竞音乐榜 15:UK排行榜 16:Billboard 17:Beatport
        18:KTV 19:iTunes 20:日本Oricon 21:Hit FM Top
        22:台湾Hito 23:欧美热歌 24:欧美新歌 25:法国NRJ Vos Hits
        26:ACG动画 27:ACG游戏 28:ACG VOCALOID 29:中国新乡村
        :param toplist_id: dictionary
        :return:[(id,name),...] toplist类型
        """
        toplist_dic = {1: 19723756, 2: 3779629, 3: 2884035, 4: 3778678, 5: 991319590, 6: 71384707, 7: 1978921795,
                       8: 2250011882, 9: 2617766278, 10: 71385702, 11: 745956260, 12: 10520166, 13: 2023401535,
                       14: 2006508653, 15: 180106, 16: 60198, 17: 3812895, 18: 21845217, 19: 11641012, 20: 60131,
                       21: 120001, 22: 112463, 23: 2809513713, 24: 2809577409, 25: 27135204, 26: 3001835560,
                       27: 3001795926, 28: 3001890046, 29: 3112516681}
        url = "http://music.163.com/discover/toplist?id=" + str(toplist_dic[toplist_id])
        html_text = self.getHtmlText(url)
        # 解析
        html_soup = BeautifulSoup(html_text, 'html.parser')
        """
        简易版本：<ul class="f-hide"></ul>之间夹住的很多个<li>标签
        复杂版本：<textarea id="song-list-pre-data" style="display:none;"></textarea>之间的JSON文件
                几千行预警~~~
                包含一首歌的名字name 别名alias 热评线commentThreadId（没啥用，就是R_SO_4_加各种的）
                作曲家 artists 专辑 album 以及很多未解析的奇怪参数
        """
        ul_tag = html_soup.find_all(attrs={'class': 'f-hide'})[0]
        toplist = []
        for single_music in ul_tag:
            toplist.append((single_music.a.attrs['href'][9:], single_music.a.string))
            # 得到类似这样的数据，列表中加元组，元组由歌曲id和歌曲名字组成
            # [('1426285166', '当遇见你'), ('1423137435', '朋友请听好'),]
            # print(single_music)
        # print(toplist)
        # print(html_text)
        return toplist

    def getAlbum(self, album_id):
        """
        获取并解析专辑内歌曲内容
        :param album_id: 专辑的id
        :return: [(id,name),...] album类型
        """
        url = "https://music.163.com/album?id=" + str(album_id)
        html_text = self.getHtmlText(url)
        html_soup = BeautifulSoup(html_text, 'html.parser')
        ul_tag = html_soup.find_all(attrs={'class': 'f-hide'})[1]  # 这个具体可能发生变化
        album = []
        for single_music in ul_tag:
            album.append((single_music.a.attrs['href'][9:], single_music.a.string))
            # 得到类似这样的数据，列表中加元组，元组由歌曲id和歌曲名字组成
            # [('1426285166', '当遇见你'), ('1423137435', '朋友请听好'),]
            # print(single_music)
        print(album)
        # print(html_text)
        return album

    def getSingerHotMusic(self, singer_id):
        """
        获取并解析歌手作曲内容
        :param singer_id:
        :return:
        """
        # https://music.163.com/artist?id=339594 mili的界面
        url = "https://music.163.com/artist?id=" + str(singer_id)
        html_text = self.getHtmlText(url)
        html_soup = BeautifulSoup(html_text, 'html.parser')
        ul_tag = html_soup.find_all(attrs={'class': 'f-hide'})[1]  # 这个具体可能发生变化
        # print(ul_tag)
        hot50 = []
        for single_music in ul_tag:
            hot50.append((single_music.a.attrs['href'][9:], single_music.a.string))
            # 得到类似这样的数据，列表中加元组，元组由歌曲id和歌曲名字组成
            # [('1426285166', '当遇见你'), ('1423137435', '朋友请听好'),]
            # print(single_music)
        print(hot50)
        # print(html_text)
        return hot50

    def getSingerAlbum(self, singer_id):
        """
        获取并解析歌手专辑
        :param singer_id:
        :return:
        """
        # https://music.163.com/#/artist/album?id=339594&limit=34&offset=0 mili的界面
        url = "https://music.163.com/artist/album?id=" + str(singer_id) + "&limit=50&offset=0"  # 一次五十个专辑
        html_text = self.getHtmlText(url)
        # print(html_text)
        html_soup = BeautifulSoup(html_text, 'html.parser')
        p_tag = html_soup.find_all(attrs={'class': 'dec dec-1 f-thide2 f-pre'})  # 这个具体可能发生变化
        # print(ul_tag)
        albumMusic = []
        for single_music in p_tag:
            albumMusic.append((single_music.a.attrs['href'][11:], single_music.attrs['title']))
            # 得到类似这样的数据，列表中加元组，元组由歌曲id和专辑名字组成
            # [('1426285166', '当遇见你'), ('1423137435', '朋友请听好'),]
            # print(single_music)
        print(albumMusic)
        # print(html_text)
        return albumMusic

    def getPlaylist(self, playlist_id):
        """
        获取并解析歌单内歌曲内容
        ！！！歌单获取不了JSON的详细信息，被加密
        :param album_id: 专辑的id
        :return: [(id,name),...] album类型
        """
        # https://music.163.com/#/playlist?id=4880844442 某个歌单页面
        url = "https://music.163.com/playlist?id=" + str(playlist_id)
        html_text = self.getHtmlText(url)
        html_soup = BeautifulSoup(html_text, 'html.parser')
        ul_tag = html_soup.find_all(attrs={'class': 'f-hide'})[1]  # 这个具体可能发生变化
        # print(ul_tag)
        playlist = []
        for single_music in ul_tag:
            playlist.append((single_music.a.attrs['href'][9:], single_music.a.string))
            # 得到类似这样的数据，列表中加元组，元组由歌曲id和歌曲名字组成
            # [('1426285166', '当遇见你'), ('1423137435', '朋友请听好'),]
            # print(single_music)
        # print(playlist)
        # print(html_text)
        return playlist

    def getMusicHotCmts_api(self, cmtThread):
        """
        获取一首歌的热门评论内容、点赞数、用户id、用户名字、时间
        :param cmtThread: string
        :return: MusicHotCmts: [{"content":str,"likes":int,"user_id":int,"user_name":str,"time",int}]
        http://music.163.com/api/v1/resource/comments/R_SO_4_516997458?limit=20&offset=0 可能活不了多久的api
        """
        limit = 20
        offset = 0
        MusicHotCmts = []
        # url 拼接
        url = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + str(cmtThread) + '?' \
              + 'limit=' + str(limit) + '&offset=' + str(offset)
        # 获取json的字符串
        json_str = self.getHtmlText(url)
        # print(json_str)
        # 写入文件来解析
        path = './cmts.txt'
        writeFile(json_str, path)
        # 解析json
        json_data = ujson.load(codecs.open('./cmts.txt', 'r', encoding='utf-8'))
        hotComments = json_data['hotComments']
        for singleCmtJson in hotComments:
            singleCmt = dict()
            singleCmt['content'] = singleCmtJson['content']
            singleCmt['likes'] = singleCmtJson['likedCount']
            singleCmt['user_id'] = singleCmtJson['user']['userId']
            singleCmt['user_name'] = singleCmtJson['user']['nickname']
            singleCmt['time'] = singleCmtJson['time']
            MusicHotCmts.append(singleCmt)
        return MusicHotCmts
        # print(json_data)
        # print(MusicHotCmts)

    def getMusicCmts_api(self, cmtThread, sum):
        """
        获取一首歌的最多sum个普通评论
        评论内容、点赞数、用户id、用户名字、时间
        :param cmtThread: string
        :param sum: int
        :return: musicCmts: [{"content":str,"likes":int,"user_id":int,"user_name":str,"time",int}]
        """
        musicCmts = []
        _sum = sum
        offset = 0
        while _sum > 0:
            if (limit := _sum % 100) == 0:  # python 3.8
                limit = 100
            # url 拼接
            url = "http://music.163.com/api/v1/resource/comments/R_SO_4_" + str(cmtThread) + '?' \
                  + 'limit=' + str(limit) + '&offset=' + str(offset)
            offset += limit
            _sum -= limit
            # 获取json的字符串
            json_str = self.getHtmlText(url)
            # print(json_str)
            # 写入文件来解析
            path = './cmts.txt'
            writeFile(json_str, path)
            # 解析json
            json_data = ujson.load(codecs.open('./cmts.txt', 'r', encoding='utf-8'))
            comments = json_data['comments']
            for singleCmtJson in comments:
                singleCmt = dict()
                singleCmt['content'] = singleCmtJson['content']
                singleCmt['likes'] = singleCmtJson['likedCount']
                singleCmt['user_id'] = singleCmtJson['user']['userId']
                singleCmt['user_name'] = singleCmtJson['user']['nickname']
                singleCmt['time'] = singleCmtJson['time']
                musicCmts.append(singleCmt)
        # return musicCmts
        # print(json_data)
        print(musicCmts)
        writeFile(str(musicCmts),"./a.txt")
        print(len(musicCmts))
