from noodles.sources.common import Source


class TestSource(Source):

    LABEL = "Test Source"
    URL = "http://test.com"

    def extract(self):
        yield self.emit(title='Test!', text='This is a test.', id='test')
