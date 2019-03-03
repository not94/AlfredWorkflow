# -*- coding:utf-8 -*-
import json
import sys


class DmhyEnumSelector(object):

    # command enum
    COMMAND_TEAM = "team"  # 联盟订阅
    COMMAND_CATEGORY = "category"  # 分类订阅

    # select ID
    SELECT_ID_MAP = {
        COMMAND_CATEGORY: "AdvSearchSort",
        COMMAND_TEAM: "AdvSearchTeam"
    }

    # enum url
    URL = "https://www.dmhy.org/topics/advanced-search?team_id=0&sort_id=0&orderby="

    def __init__(self, command):
        self.command = command
        self._data = None

    def _get_from_web(self):
        import requests_html
        s = requests_html.HTMLSession()
        r = s.get(self.URL)
        status_code = r.status_code
        if status_code == 200:
            self._data = {}
            for command, select_id in self.SELECT_ID_MAP.items():
                self._data[command] = {}
                select_element = r.html.find(
                    "select#{}".format(select_id), first=True
                )
                for option_element in select_element.find("option"):
                    self._data[command][option_element.text] = \
                        option_element.attrs['value']

    def _get_from_local(self):
        self._data = dict()
        self._data[self.COMMAND_CATEGORY] = {
            '全部': '0',
            '動畫': '2',
            '季度全集': '31',
            '漫畫': '3',
            '港台原版': '41',
            '日文原版': '42',
            '音樂': '4',
            '動漫音樂': '43',
            '同人音樂': '44',
            '流行音樂': '15',
            '日劇': '6',
            'ＲＡＷ': '7',
            '遊戲': '9',
            '電腦遊戲': '17',
            '電視遊戲': '18',
            '掌機遊戲': '19',
            '網絡遊戲': '20',
            '遊戲周邊': '21',
            '特攝': '12',
            '其他': '1'
        }
        self._data[self.COMMAND_TEAM] = {
            '全部': '0',
            '動漫花園': '117',
            '动漫国字幕组': '303',
            '极影字幕社': '185',
            '咪梦动漫组': '710',
            '悠哈C9字幕社': '151',
            '喵萌奶茶屋': '669',
            '天使动漫论坛': '390',
            'LoliHouse': '657',
            '喵萌茶会字幕组': '468',
            '雪飄工作室(FLsnow)': '37',
            'DHR動研字幕組': '407',
            'c.c动漫': '604',
            'c-a Raws': '695',
            '漫貓字幕組': '423',
            '风之圣殿': '434',
            '幻樱字幕组': '241',
            '八重樱字幕组': '663',
            '千夏字幕组': '283',
            '诸神kamigami字幕组': '288',
            '桜都字幕组': '619',
            '漫游字幕组': '134',
            'ANK-Raws': '375',
            'LoveEcho!': '504',
            '天行搬运': '602',
            '時雨初空': '570',
            'YMDR发布组': '720',
            '西农YUI汉化组': '525',
            '青森小镇': '708',
            '风车字幕组': '454',
            'ZERO字幕组': '391',
            '动音漫影': '88',
            'TUcaptions': '492',
            '白恋字幕组': '438',
            '豌豆字幕组': '520',
            '波洛咖啡厅': '627',
            '飞龙骑脸字幕组(G.I.A.N.T)': '709',
            '澄空学园': '58',
            '届恋字幕组': '703',
            '爱恋字幕社': '47',
            '轻之国度': '321',
            '未央阁联盟': '592',
            '枫叶字幕组': '630',
            '楓雪連載製作': '34',
            '幻之字幕组': '430',
            '银色子弹字幕组': '576',
            '东京不够热': '526',
            '新番字幕组': '672',
            '天空树双语字幕组': '485',
            '追新番字幕组': '651',
            'VRAINSTORM': '673',
            '银光字幕组': '506',
            '梦星字幕组': '552',
            'WOLF字幕组': '141',
            '聖域字幕組': '403',
            '小愿8压制组': '705',
            '魯邦聯會': '721',
            '动漫先锋': '104',
            'NEO·QSW': '537',
            'AikatsuFans': '675',
            'VCB-Studio': '581',
            'BBA字幕组': '436',
            'KRL字幕组': '228',
            '小花花同盟戰線': '699',
            'AQUA工作室': '217',
            '梦蓝字幕组': '574',
            '鈴風字幕組': '225',
            '萝莉社活动室': '550',
            '80v08': '719',
            'LittleBakas!': '638',
            '脸肿字幕组': '568',
            '花園壓制組': '563',
            '旋风字幕组': '370',
            '漫藤字幕组': '559',
            '省电Raws': '631',
            '华盟字幕社': '49',
            '柯南事务所': '75',
            '天香字幕社': '110',
            '虐心发布组': '690',
            '冷番补完字幕组': '641',
            '雪梦字幕组': '567',
            'Little字幕组': '680',
            '乐园字幕组': '723',
            'Centaurea-Raws': '573',
            '自由字幕组': '432',
            'Astral Union字幕组': '716',
            '魔星字幕团': '648',
            'Vmoe字幕組': '536',
            'NAZOrip': '697',
            '狐狸小宮': '701',
            '囧夏发布组': '507',
            '虚数学区研究协会': '664',
            'AZT字幕组': '717',
            'CureSub': '332',
            '钉铛字幕组': '561',
            'SFEO-Raws': '652',
            'EggPainRaws': '541',
            '天空字幕组': '453',
            '天の翼字幕汉化社': '606',
            '紫音動漫&發佈組': '459',
            '星火字幕组': '558',
            '驯兽师联盟': '626',
            'BlueRabbit': '687',
            '夜莺工作室': '394',
            '矢车菊影音工作室': '505',
            'TenYun': '702'
        }

    def init_data(self):
        if self._data is not None:
            return
        self._get_from_local()

    def serialize(self):
        self.init_data()
        data = self._data.get(self.command, {})
        return json.dumps(
            {
                "items": [
                    {
                        "title": title,
                        "arg": value
                    }
                    for title, value in data.items()
                ]
            },
            ensure_ascii=False
        )


if __name__ == '__main__':
    command = sys.argv[1]
    print(DmhyEnumSelector(command).serialize())
