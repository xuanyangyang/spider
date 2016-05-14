import urllib.request
import re


class Iplist:
    def __init__(self, url):
        self.url = url
        self.reLine = re.compile(r'<td>(?:(?:[0,1]?\d?\d?|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d?|2[0-4]\d|25[0-5])</td>'
                                 r'\s*<td>(?:\d?){4}</td>')
        self.reIp = re.compile(r'(?:(?:[0,1]?\d?\d?|2[0-4]\d|25[0-5])\.){3}(?:[0,1]?\d?\d?|2[0-4]\d|25[0-5])')
        self.rePort = re.compile(r'<td>(\d?\d?\d?\d?)</td>')

    def get_page(self):
        req = urllib.request.Request(self.url)
        req.add_header('User-Agent',
                       "Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4")
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')

        return html

    def get_ip_list(self):
        """
        先获得有关于IP以及port一行的内容
        然后再提取IP和port组合成IP:port形式
        """
        lines = self.reLine.findall(self.get_page())
        iplist = []
        for ip in lines:
            iplist.append(self.reIp.findall(ip)[0] + ':' + self.rePort.findall(ip)[0])

        return iplist

if __name__ == '__main__':
    iplist = Iplist('http://www.xicidaili.com/nn')
    lists = iplist.get_ip_list()
    for ip in lists:
        print(ip)

