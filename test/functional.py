import unittest
from pyg_annotate.lib.generate_annotations import annotate


class AnnoTests(unittest.TestCase):

    def setUp(self):
        from pyg_annotate.test.testcase import sourcestr
        self.source, self.annos = annotate(sourcestr, "Python")
        print(self.source, self.annos)

    def test_types(self):
        self.assertTrue(isinstance(self.source, str))
        self.assertTrue(isinstance(self.annos, list))
        for anno in self.annos:
            self.assertTrue(isinstance(anno, dict))

if __name__ == "__main__":
    unittest.main()
