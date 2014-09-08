import unittest
import mock
import IEDTemplate

class TemplateTests(unittest.TestCase):
  def setUp(self):
    self.template = IEDTemplate.IEDTemplate.alloc().init()

if __name__ == '__main__':
  unittest.main()
