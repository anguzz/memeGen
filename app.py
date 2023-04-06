import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QFileDialog, QColorDialog
from PyQt6.QtGui import QPixmap, QPainter, QFont, QColor
from PyQt6.QtCore import Qt


class ImageCaptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('memeGen')

        # widgets
        self.image_label = QLabel()
        self.caption_edit = QLineEdit()
        self.upload_button = QPushButton('Upload Image')
        self.save_button = QPushButton('Save image with caption')
        self.color_button = QPushButton('Caption Color')

        # map buttons to functions
        self.upload_button.clicked.connect(self.upload_image)
        self.save_button.clicked.connect(self.save_image)
        self.color_button.clicked.connect(self.choose_color)
        
        # default color to white
        self.caption_color = QColor(255, 255, 255)

        # layouts
        image_lay = QVBoxLayout()
        image_lay.addWidget(self.image_label)
        image_lay.addWidget(self.upload_button)

        caption_lay = QHBoxLayout()
        caption_lay.addWidget(QLabel('Caption:'))
        caption_lay.addWidget(self.caption_edit)
        caption_lay.addWidget(self.save_button)

        color_lay = QHBoxLayout()
        color_lay.addWidget(self.color_button)

        main_lay = QVBoxLayout()
        main_lay.addLayout(image_lay)
        main_lay.addLayout(caption_lay)
        main_lay.addLayout(color_lay)

        self.setLayout(main_lay)

    def upload_image(self):
        # open file dialog and select path
        file_dialog = QFileDialog()
        file_dialog.setNameFilter('Image files (*.jpg *.png *.bmp)')
        if file_dialog.exec():
            file_path = file_dialog.selectedFiles()[0]
            self.display_image(file_path)

    def display_image(self, file_path):
        # load image file then display it
        pixmap = QPixmap(file_path)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    def save_image(self):
        # get text and draw it onto the image when saving
        caption = self.caption_edit.text()
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            painter = QPainter(pixmap)
            painter.setPen(self.caption_color)
            font = QFont('Arial', 20)
            font.setPointSize(font.pointSize() + 10)
            painter.setFont(font)
            #align the caption to the bottom
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom, caption)
            painter.end()

            # save image w caption to file
            file_dialog = QFileDialog()
            file_dialog.setDefaultSuffix('png')
            file_dialog.setNameFilter('PNG files (*.png)')
            if file_dialog.exec():
                file_path = file_dialog.selectedFiles()[0]
                pixmap.save(file_path)

    def choose_color(self):
        # uses color dialog to choose color
        color_dialog = QColorDialog()
        color = color_dialog.getColor()
        if color.isValid():
            self.caption_color = color

    def resizeEvent(self, event):
        # scale image to fit window, mayb change later to normalize image somehow as large images can make window v huge
        pixmap = self.image_label.pixmap()
        if pixmap is not None:
            self.image_label.setPixmap(pixmap.scaled(self.image_label.width(), self.image_label.height()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    image_caption_app = ImageCaptionApp()
    image_caption_app.show()
    palette = app.palette()

    darkgrey= '#7393B3'
    lightblue='#EAEAEA'
    black='#151a1c'
    white='#FFFFFF'

    palette.setColor(palette.ColorRole.Window, QColor(black))

    palette.setColor(palette.ColorRole.WindowText, QColor(white)) 
    palette.setColor(palette.ColorRole.Base, QColor(black))
    palette.setColor(palette.ColorRole.AlternateBase, QColor(black))
    palette.setColor(palette.ColorRole.ToolTipBase, QColor(black))
    palette.setColor(palette.ColorRole.ToolTipText, Qt.GlobalColor.black)
    palette.setColor(palette.ColorRole.Text, QColor(black))
    palette.setColor(palette.ColorRole.Button, QColor(black))
    palette.setColor(palette.ColorRole.ButtonText, Qt.GlobalColor.black)
    palette.setColor(palette.ColorRole.BrightText, QColor(black))
    palette.setColor(palette.ColorRole.Link, QColor(lightblue))
    app.setPalette(palette)
    sys.exit(app.exec())
