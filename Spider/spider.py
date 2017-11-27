import urllib2
import urllib
import re


def get_html(url):
    page = urllib2.urlopen(url)
    html = page.read()
    return html


def get_image(html):
    pattern = r'src="(.*?\.jpg)" bdwater='
    image = re.compile(pattern)
    image_list = re.findall(image, html)
    i = 0
    for imgurl in image_list:
        urllib.urlretrieve(imgurl, r'C:\Users\ts\Pictures\%s.jpg' % i)
        i += 1


html = get_html('http://tieba.baidu.com/p/2166231880')
print get_image(html)
