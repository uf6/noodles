import logging
import requests
from lxml import html, etree

from noodles.sources.common import Source

RSS_FEED = 'http://www.rigzone.com/news/rss/rigzone_latest.aspx'
PAGE_URL = 'http://www.rigzone.com/news/article_pf.asp?a_id=%s'
log = logging.getLogger(__name__)


class RigZoneSource(Source):

    LABEL = "RigZone"
    URL = "http://www.rigzone.com/"

    def extract(self):
        feed = etree.parse(RSS_FEED)
        url = feed.findtext('.//item/link')
        id = int(url.split('/a/', 1)[-1].split('/', 1)[0])
        for article_id in xrange(id, 1, -1):
            url = PAGE_URL % article_id
            id = self.check(url=url)
            if id is not None:
                yield id
                continue

            res = requests.get(url)
            doc = html.fromstring(res.content)

            title = None
            for span in doc.findall('.//span'):
                if 'font-size:12pt;font-weight:bold;' in span.get('style'):
                    title = span.text_content().strip()
                    break

            if title is None:
                continue

            log.info('RigZone: %s', title)

            text = doc.text_content()
            yield self.emit(title=title, text=text,
                            url=url)
