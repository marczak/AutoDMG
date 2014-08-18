import unittest
import mock
import IEDLog


class UtilTests(unittest.TestCase):

  def setUp(self):
    self.util = IEDLog.IEDLog

  def testAddMessage_level_(self, message, level):
    logLine = IEDLogLine.alloc().initWithMessage_level_(message, level)
    self.logLines.append(logLine)
    if defaults.integerForKey_(u"LogLevel") >= level:
      self.visibleLogLines.append(logLine)
      if self.logTableView:
        self.logTableView.reloadData()
        if self.logAtBottom:
          self.logTableView.scrollRowToVisible_(len(self.visibleLogLines) - 1)



  # Act on user showing log window.

  @LogException
  @IBAction
  def testDisplayLogWindow_(self, sender):
    self.logAtBottom = True
    self.logTableView.scrollRowToVisible_(len(self.visibleLogLines) - 1)
    self.logWindow.makeKeyAndOrderFront_(self)



  # Act on notification for log being scrolled by user.

  def testLogViewScrolled_(self, notification):
    tableViewHeight = self.logTableView.bounds().size.height
    scrollView = self.logTableView.enclosingScrollView()
    scrollRect = scrollView.documentVisibleRect()
    scrollPos = scrollRect.origin.y + scrollRect.size.height
    
    if scrollPos >= tableViewHeight:
      self.logAtBottom = True
    else:
      self.logAtBottom = False

  # Act on user filtering log.

  @LogException
  @IBAction
  def testSetLevel_(self, sender):
    self.visibleLogLines = [x for x in self.logLines if x.level() <= self.levelSelector.indexOfSelectedItem()]
    self.logAtBottom = True
    self.logTableView.reloadData()
    self.logTableView.scrollRowToVisible_(len(self.visibleLogLines) - 1)



  # Act on user clicking save button.

  @LogException
  @IBAction
  def testSaveLog_(self, sender):
    panel = NSSavePanel.savePanel()
    panel.setExtensionHidden_(False)
    panel.setAllowedFileTypes_([u"log", u"txt"])
    formatter = NSDateFormatter.alloc().init()
    formatter.setDateFormat_(u"yyyy-MM-dd HH.mm")
    dateStr = formatter.stringFromDate_(NSDate.date())
    panel.setNameFieldStringValue_(u"AutoDMG %s" % dateStr)
    result = panel.runModal()
    if result != NSFileHandlingPanelOKButton:
      return
    
    exists, error = panel.URL().checkResourceIsReachableAndReturnError_(None)
    if exists:
      success, error = NSFileManager.defaultManager().removeItemAtURL_error_(panel.URL(), None)
      if not success:
        NSApp.presentError_(error)
        return
    
    success, error = NSData.data().writeToURL_options_error_(panel.URL(), 0, None)
    if not success:
      NSApp.presentError_(error)
      return
    
    fh, error = NSFileHandle.fileHandleForWritingToURL_error_(panel.URL(), None)
    if fh is None:
      NSAlert.alertWithError_(error).runModal()
      return
    formatter = NSDateFormatter.alloc().init()
    formatter.setDateFormat_(u"yyyy-MM-dd HH:mm:ss")
    for logLine in self.logLines:
      textLine = NSString.stringWithFormat_(u"%@ %@: %@\n",
                                            formatter.stringFromDate_(logLine.date()),
                                            IEDLogLevelName(logLine.level()),
                                            logLine.message())
      fh.writeData_(textLine.dataUsingEncoding_(NSUTF8StringEncoding))
    fh.closeFile()



  # We're an NSTableViewDataSource.

  def testNumberOfRowsInTableView_(self, tableView):
    return len(self.visibleLogLines)

  def testTableView_objectValueForTableColumn_row_(self, tableView, column, row):
    if column.identifier() == u"date":
      return self.visibleLogLines[row].date()
    elif column.identifier() == u"level":
      return IEDLogLevelName(self.visibleLogLines[row].level())
    elif column.identifier() == u"message":
      return self.visibleLogLines[row].message()