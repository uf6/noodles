from noodles.sources.test import TestSource
from noodles.sources.edgar import EdgarSource
from noodles.sources.openoil import OpenOilSource
from noodles.sources.allafrica import AllAfricaSource
from noodles.sources.rigzone import RigZoneSource


SOURCES = {
    'test': TestSource,
    'allafrica': AllAfricaSource,
    'openoil': OpenOilSource,
    'edgar': EdgarSource,
    'rigzone': RigZoneSource
}


def extract(source):
    source = SOURCES[source](source)
    for document_id in source.extract():
        yield document_id
