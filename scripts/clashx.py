# -*- coding: utf-8 -*
import sys
import os
import asyncio
from lib import requests

from functools import wraps, partial


def async_wrap(func):
    @wraps(func)
    async def run(*args, loop=None, executor=None, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        pfunc = partial(func, *args, **kwargs)
        return await loop.run_in_executor(executor, pfunc)
    return run


class ProxyDelayQuery(object):

    BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:9090")

    @async_wrap
    def doQuery(self, name):
        delay_test_params = {
            "timeout": os.environ.get("delay_test_timeout", 1000),
            "url": os.environ.get(
                "delay_test_url", "http://cp.cloudflare.com/generate_204"
            )
        }
        resp = requests.get(
            self.BASE_URL + "/proxies/" + name + "/delay",
            params=delay_test_params
        )
        if not resp.ok:
            return {}
        return {
            "name": name,
            "ms": resp.json().get("delay", 0)
        }

    async def main(self, proxy_node_names):
        tasks = []
        for name in proxy_node_names:
            tasks.append(asyncio.create_task(self.doQuery(name)))
        return await asyncio.gather(*tasks)

    def get_min_delay_info(self, proxy_node_names):
        infos = asyncio.run(self.main(proxy_node_names))
        min_delay_info = {
            "name": "",
            "ms": 10000
        }
        for info in infos:
            if 0 < info.get("ms", 0) < min_delay_info.get("ms"):
                min_delay_info = info
        return min_delay_info


class ClashXAutomation(object):

    COMMAND_GLOBAL_SWITCH = "Global"
    COMMAND_RULE_SWITCH = "Rule"
    COMMAND_AUTO_SWITCH = "Auto"

    DEFAULT_MODE = "Rule"

    BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:9090")
    COMMON_CONFIG_URL = BASE_URL + "/configs"
    PROXIES_URL = BASE_URL + "/proxies"

    def switch_proxy(self, command):
        data = {
            "mode": command
        }
        resp = requests.patch(self.COMMON_CONFIG_URL, json=data)
        notification = u"VPN切换" + command + u"代理"
        if resp.ok:
            status = u"成功"
        else:
            status = u"失败"
        return notification + status

    def switch_fastest_proxy(self):
        resp = requests.get(self.COMMON_CONFIG_URL)
        if not resp.ok:
            return u"查询基础配置失败: {}".format(resp.text)
        current_mode = resp.json().get('mode', self.DEFAULT_MODE)
        if current_mode == 'global':
            current_proxy_name = "GLOBAL"
        else:
            current_proxy_name = os.environ.get("proxy_name", "BosLife")

        resp = requests.get(self.PROXIES_URL)
        if not resp.ok:
            return u"查询所有代理信息失败"
        data = resp.json()
        proxy_node_names = data.get('proxies', {})\
            .get(current_proxy_name, {})\
            .get('all', [])

        # sync query delay
        # min_delay_ms = 10000
        # min_delay_name = ""
        # delay_test_params = {
        #     "timeout": os.environ.get("delay_test_timeout", 1000),
        #     "url": os.environ.get(
        #         "delay_test_url", "http://cp.cloudflare.com/generate_204"
        #     )
        # }
        # for name in proxy_node_names:
        #     resp = requests.get(
        #         self.BASE_URL + "/proxies/" + name + "/delay",
        #         params=delay_test_params
        #     )
        #     if not self.is_success_response(resp, self.SUCCESS_GET_CODE):
        #         continue
        #     delay_ms = resp.json().get("delay", 0)
        #     if 0 < delay_ms < min_delay_ms:
        #         min_delay_ms = delay_ms
        #         min_delay_name = name

        # async query delay
        min_delay_info = ProxyDelayQuery().get_min_delay_info(proxy_node_names)
        min_delay_name = min_delay_info.get("name")
        min_delay_ms = min_delay_info.get("ms")
        if not min_delay_name:
            return u"查询代理延迟时间失败"

        resp = requests.put(
            self.PROXIES_URL + "/" + current_proxy_name,
            json={"name": min_delay_name}
        )
        if resp.ok:
            return u"切换代理" + min_delay_name + u"({}ms)成功".format(min_delay_ms)
        else:
            return u"切换代理失败: " + resp.text

    def process(self, command):
        if command in [self.COMMAND_GLOBAL_SWITCH, self.COMMAND_RULE_SWITCH]:
            return self.switch_proxy(command)
        elif self.COMMAND_AUTO_SWITCH == command:
            return self.switch_fastest_proxy()
        else:
            return u"无效的命令{}".format(command)


if __name__ == '__main__':
    command = "".join(sys.argv[1:])
    print(ClashXAutomation().process(command))
