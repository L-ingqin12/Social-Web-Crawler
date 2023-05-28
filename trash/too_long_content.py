from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QItemDelegate
from PyQt5.QtGui import QPainter, QColor, QFont, QTextOption, QFontMetrics
from PyQt5.QtCore import Qt, QRectF

class TextEllipsisDelegate(QItemDelegate):
    def paint(self, painter, option, index):
        if index.data():
            painter.save()
            options = QTextOption()
            options.setWrapMode(QTextOption.Clip)
            options.setAlignment(option.displayAlignment)
            font = QFont(option.font)
            fontMetrics = QFontMetrics(font)
            rect = option.rect.adjusted(0,0,-4,0)
            text = fontMetrics.elidedText(index.data(), Qt.ElideRight, rect.width())
            painter.drawText(rect, options, text)
            painter.restore()
        else:
            super(TextEllipsisDelegate, self).paint(painter, option, index)

class MyTableWidget(QTableWidget):
    def __init__(self, *args, **kwargs):
        super(MyTableWidget, self).__init__(*args, **kwargs)
        delegate = TextEllipsisDelegate(self)
        self.setItemDelegate(delegate)
        self.setStyleSheet('''
            QTableWidget::item{
              border-bottom:1px solid #d9d9d9;
              border-right:1px solid #d9d9d9;
              padding:2px 5px 2px 5px;
              background-color: #ffffff;
              color: #000000;
            }
            QTableWidget::item:selected{
              background-color: #357ae8;
              color: #ffffff;
              border-bottom: 1px solid #294c73;
              border-right:none;
            }
        ''')
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

if __name__ == '__main__':
    app = QApplication([])
    table = MyTableWidget()
    table.setRowCount(1)
    table.setColumnCount(1)
    table.setItem(0, 0, QTableWidgetItem('This is a very long text which needs to be truncated.'))
    table.resizeColumnsToContents()
    table.resizeRowsToContents()
    table.show()
    app.exec_()
