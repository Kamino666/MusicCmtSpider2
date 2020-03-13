from Spider.NeteaseMusic import NeteaseMusic


def main():
    # url = r"http://music.163.com/discover/toplist?id=19723756"  # 获取热门榜单的url 正常
    # ?order=hot&cat=全部&limit=35&offset=0 可选参数
    # order是顺序 cat是分类 limit最大是35 offset是偏移量
    url = r"http://music.163.com/discover/playlist"  # 获取热门歌曲的url
    # 其他url大同小异
    NEspider = NeteaseMusic()
    NEspider.getMusicCmts_api(435166266, 20)


if __name__ == "__main__":
    main()
