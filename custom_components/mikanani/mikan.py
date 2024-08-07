from html.parser import HTMLParser
from dataclasses import dataclass
from enum import Enum

from .const import MIKAN_HOST

type MikanParseResult = dict[int | str, list[MikanBangumi]]


class ParseStates(Enum):
    START = 0
    DAILY_ENTRY = 1
    BANGUMI_ENTRY = 2


@dataclass
class MikanBangumi:
    id: int
    title: str
    link: str
    image_link: str
    subscribed: bool

    def __init__(self) -> None:
        self.id: int = 0
        self.title: str = ""
        self.link: str = ""
        self.image_link: str = ""
        self.subscribed: bool = False


class MikanHTMLParser(HTMLParser):
    """MikanHTMLParser: 解析 Mikanani 网页番剧信息。

    Usage:
        html_text = request_func(MIKAN_HOST)
        parser = MikanHTMLParser()
        parser.feed(html_text)
        print(parser.parse_result)

    使用简陋的有限状态机实现番剧信息的提取。
    提取结果类型为 dict[str, list[MikanBangumi]]，该字典的值是一个MikanBangumi列表，
    键通常是一个一位十进制数字，代表星期N/剧场版。0-6代表从周日开始的一周，7代表剧场版。
        0-6: 周日-周六
        7  : 剧场版
    """

    def __init__(self) -> None:
        super().__init__()

        self._bangumi_map : MikanParseResult = {}

        self._state = ParseStates.START
        self._week = ""

    @property
    def _bangumi(self) -> MikanBangumi:
        """当前正需记录信息的番剧"""
        return self._bangumi_map[self._week][-1]

    @property
    def parse_result(self) -> MikanParseResult:
        """解析结果"""
        return self._bangumi_map

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        """从标签解析信息"""

        # 不需要考虑重 key 的问题，所以转成 dict
        attributes = dict(attrs)

        # 一周番剧列表从 div 开始
        if tag == 'div':
            # 如果 div 有 data-dayofweek 属性则设状态为 DAILY_ENTRY
            if (week := attributes.get("data-dayofweek")) is not None:
                self._state = ParseStates.DAILY_ENTRY
                # 记录 week 编号
                # 0-6 为周日-周六
                # 7   为剧场版
                self._week = int(week) if str.isdigit(week) else week
                # 初始化本周番剧列表为空数组
                if not self._bangumi_map.get(week):
                    self._bangumi_map[self._week] = []

        # 番剧从 li 开始
        if self._state == ParseStates.DAILY_ENTRY and tag == "li":
            # 设状态为 BANGUMI_ENTRY
            self._state = ParseStates.BANGUMI_ENTRY
            # 初始化 MikanBangumi，之后填空
            self._bangumi_map[self._week].append(MikanBangumi())

        # 当状态为 BANGUMI_ENTRY，开始记录番剧信息
        if self._state == ParseStates.BANGUMI_ENTRY:
            if tag == "span":
                # 封面图片链接
                if (image_link := attributes.get("data-src")) is not None:
                    self._bangumi.image_link = MIKAN_HOST + image_link
                # 是否已订阅
                self._bangumi.subscribed = attributes.get("data-showsubscribed") == "true"
                # bangumi id, 如果是数字才记录
                if (id := attributes.get("data-bangumiid")) is not None and str.isdigit(id):
                    self._bangumi.id = int(id)
            # 以防万一有多个a标签，要的是有title属性的a标签
            elif tag == "a" and (title := attributes.get("title")) is not None:
                # 番剧链接
                if (link := attributes.get("href")) is not None:
                    self._bangumi.link = MIKAN_HOST + link
                # 番剧标题
                self._bangumi.title = title

    def handle_endtag(self, tag):
        # 当 li 闭合的时候结束 BANGUMI_ENTRY，回到 DAILY_ENTRY
        if self._state == ParseStates.BANGUMI_ENTRY and tag == "li":
            self._state = ParseStates.DAILY_ENTRY
