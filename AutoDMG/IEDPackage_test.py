import unittest
import mock
import IEDPackage

class PackageTests(unittest.TestCase):
  def setUp(self):
    self.package = IEDPackage.IEDPackage.alloc().init()
    self.package.init()

  def testName(self):
    self.package.setName_('woo')
    self.assertEquals(self.package.name(), 'woo')

  def testPath(self):
    self.package.setPath_('yay')
    self.assertEquals(self.package.path(), 'yay')

  def testSize(self):
    self.package.setSize_(12)
    self.assertEquals(self.package.size(), 12)

  def testUrl(self):
    self.package.setUrl_('http://www.apple.com')
    self.assertEquals(self.package.url(), 'http://www.apple.com')

  def testImage(self):
    self.package.setImage_('image.dmg')
    self.assertEquals(self.package.image(), 'image.dmg')

  def testSha1(self):
    self.package.setSha1_('810f4b57d2112a4176c4241197f67ff4c5c6009c')
    self.assertEquals(self.package.sha1(), '810f4b57d2112a4176c4241197f67ff4c5c6009c')


if __name__ == '__main__':
  unittest.main()
