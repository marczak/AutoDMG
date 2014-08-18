import unittest
import mock
import IEDUtil


class UtilTests(unittest.TestCase):

  def setUp(self):
    self.util = IEDUtil.IEDUtil

  def testReadSystemVersion_(self):
    IEDUtil.NSDictionary = mock.MagicMock()
    plist = {u'ProductName': 'OS X',
             u'ProductUserVisibleVersion': '10',
             u'ProductBuildVersion': '5'}
    IEDUtil.NSDictionary.dictionaryWithContentsOfFile_.return_value = plist
    result = self.util.readSystemVersion_(u'/foo/bar')
    self.assertEqual(result, (plist[u'ProductName'],
                              plist[u'ProductUserVisibleVersion'],
                              plist[u'ProductBuildVersion']))

  def testGetAppVersion(self):
    version = {u'CFBundleShortVersionString': '1985',
               u'CFBundleVersion': '1985.125'}

    def side_effect(value):
      if value in version:
        return version[value]
      else:
        return DEFAULT

    IEDUtil.NSBundle.objectForInfoDictionaryKey_ = mock.MagicMock(side_effect=
                                                                  side_effect)
    result = self.util.getAppVersion()
    self.assertEqual(result, (version[u'CFBundleShortVersionString'],
                              version[u'CFBundleVersion']))

  def testResolvePath(self):
    fsref = mock.MagicMock()
    IEDUtil.FSResolveAliasFile = mock.MagicMock()
    IEDUtil.FSResolveAliasFile.return_value = (fsref, True, False)
    IEDUtil.os.path.abspath = mock.MagicMock()
    IEDUtil.os.path.abspath.return_value = u'/other/path'
    self.assertEqual(self.util.resolvePath_(u'/foo/bar'), u'/other/path')

  def testResolvePathFails(self):
    IEDUtil.FSResolveAliasFile = mock.MagicMock(side_effect=IEDUtil.MacOS.Error)
    self.assertIsNone(self.util.resolvePath_(u'/foo/bar'))

  def testInstallESDPath(self):
    """
      I can't figure out how to test this method. It calls a class method and nothing I've tried
      will mock that successfully.
    """
    pass



if __name__ == '__main__':
  unittest.main()
