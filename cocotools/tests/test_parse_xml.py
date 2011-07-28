#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

# Stdlib
import xml.etree.ElementTree as etree

# Third party
from mocker import MockerTestCase

# Local
import cocotools.parse_xml as cpx

#------------------------------------------------------------------------------
# Test Classes
#------------------------------------------------------------------------------

class TestXMLReader(MockerTestCase):

    def setUp(self):
        f = open('cocotools/tests/sample_map.xml')
        self.xml_string = f.read()
        f.seek(0)
        self.f = f
        self.tag_prefix = './/{http://www.cocomac.org}'

    def tearDown(self):
        self.f.close()

    def test_string2primiter(self):
        # Because string2primiter is called upon the instantiation of
        # XMLReader, this will serve as a test of __init__ as well.
        prefix = self.tag_prefix
        reader = cpx.XMLReader('Mapping', self.xml_string)
        self.assertEqual(reader.prim_tag, 'PrimaryRelation')
        self.assertEqual(reader.tag_prefix, prefix)
        self.assertEqual(reader.prim_iterator.next().tag,
                         '%sPrimaryRelation' % prefix[3:])
        self.assertEqual(reader.search_string,
                         "('PP99')[SOURCEMAP]OR('PP99')[TARGETMAP]")

    def test_prim2data(self):
        prefix = self.tag_prefix
        prim = etree.parse(self.f).find('%sPrimaryRelation' % prefix)
        mocker = self.mocker
        reader = mocker.mock()
        reader.tag_prefix
        mocker.result(prefix)
        reader.prim_tag
        mocker.result('PrimaryRelation')
        mocker.replay()
        self.assertEqual(cpx.XMLReader.prim2data.im_func(reader, prim),
                         ('B05-19', 'PP99-19',
                          {'RC': ['I'], 'PDC': ['P'], 'TP': [[]]}))