import logging
import requests
import mwclient
from lxml import html

from noodles.sources.common import Source

log = logging.getLogger(__name__)


class OpenOilSource(Source):

    LABEL = "OpenOil Repository"
    URL = "http://repository.openoil.net/"

    def extract(self):
        site = mwclient.Site('repository.openoil.net')
        for page in site.Pages:
            page_url = 'http://repository.openoil.net/w/index.php'
            res = requests.get(page_url, params={'action': 'view',
                                                 'title': page.name})
            doc = html.fromstring(res.content)
            el = doc.find('.//div[@id="bodyContent"]')
            log.info("Extract from %s, %s", page.name, res.url)
            yield self.emit(title=page.name, text=el.text_content(),
                            url=res.url)
