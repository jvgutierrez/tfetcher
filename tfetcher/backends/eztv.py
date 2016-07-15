import requests
from bs4 import BeautifulSoup
import re
from functools import lru_cache


class EztvFetcher(object):
    def __init__(self, base_url="https://eztv.ag"):
        self.base_url = base_url

    @lru_cache(maxsize=32)
    def _fetch_url(self, url):
        try:
            req = requests.get("{0}{1}".format(self.base_url, url))
            if req.ok:
                return BeautifulSoup(req.text, "html.parser")
        except Exception as e:
            raise e

    def _episode_regex(self, season, episode, quality):
        return re.compile('(S{0:02d}E{1:02d}|{0}x{1:02d}) {2}'.format(season,
                                                                      episode,
                                                                      quality))

    def getTorrentLink(self, show, season, episode, quality):
        self.showlist = self._fetch_url("/showlist/")
        show_link = self.showlist.find("a", class_="thread_link", string=show)
        if show_link is not None:
            show_page = self._fetch_url(show_link.attrs['href'])
            episode = show_page.find("a",
                                     class_="magnet",
                                     title=self._episode_regex(season,
                                                               episode,
                                                               quality))
            if episode is not None:
                return episode.attrs['href']
            return None
