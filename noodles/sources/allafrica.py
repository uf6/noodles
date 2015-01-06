import os
import logging
import requests
from lxml import html
from urlparse import urljoin
from werkzeug.utils import secure_filename

from noodles.sources.common import Source
from noodles.util import stage_path

log = logging.getLogger(__name__)


class AllAfricaSource(Source):

    LABEL = "AllAfrica"
    URL = "http://allafrica.com/"

    def get_article(self, url):
        file_name = secure_filename(url)
        file_path = os.path.join(stage_path(self.name, 'stories'), file_name)
        if not os.path.isfile(file_path):
            try:
                os.makedirs(os.path.dirname(file_path))
            except:
                pass
            with open(file_path, 'wb') as fh:
                res = requests.get(url)
                fh.write(res.content)

        with open(file_path, 'rb') as fh:
            doc = html.parse(fh)
            el = doc.find('.//div[@class="section article"]')
            title = el.findtext('.//h1').strip()
            text = el.find('.//div[@class="story-body"]')
            if text is not None:
                text = text.text_content()
            log.info("Scraped: %s, %s", title, url)
            return self.emit(title=title, text=text, url=url)

    def extract(self):
        url_base = 'http://allafrica.com/latest/?page=%s'
        for i in xrange(1, 1000):
            url = url_base % i
            res = requests.get(url)
            doc = html.fromstring(res.content)
            for a in doc.findall('.//a'):
                article_url = urljoin(url, a.get('href', '/'))
                if 'allafrica.com/stories/' not in article_url:
                    continue
                yield self.get_article(article_url)

        
