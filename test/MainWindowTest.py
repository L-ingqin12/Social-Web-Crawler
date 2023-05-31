import unittest
from PyQt5.QtWidgets import QApplication
from app.view.main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])
        self.window = MainWindow()

    def test_switchTo(self):
        # test switchTo method
        self.window.switchTo(self.window.settingInterface, False)
        self.assertEqual(self.window.stackWidget.currentWidget(), self.window.settingInterface)

    def tearDown(self):
        self.window.close()
        del self.window
        del self.app

if __name__ == '__main__':
    unittest.main()

