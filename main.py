import os
import threading
import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from ebookhandler import Bookshelf

WIDTH = 256
HEIGHT = 512
KINDLE_PATH = "/Volumes/Kindle/"
TRANSFERING = False


class Gui:
    def __init__(self, guiItems):
        self.guiItems = guiItems

    def setLabelText(self, id, text):
        self.guiItems[id].text = text

    def getGuiItem(self, id):
        return self.guiItems[id]


class EbookHandler(Widget):
    def __init__(self, **kwargs):
        super(EbookHandler, self).__init__(**kwargs)
        self.kindleDisabled = True
        self.isTransfering = False
        self.bookshelf = Bookshelf()
        self.bookshelf.setup()
        self.gui = Gui(self.ids)
        self.setup()
        self.__setThreads__()

    def findKindle(self):
        if os.path.isdir(KINDLE_PATH):
            self.kindleDisabled = False
            return "Kindle Connected"
        else:
            self.kindleDisabled = True
            return "No Kindle Detected"

    def pollDevice(self):
        while True:
            self.findKindle()
            time.sleep(2)
            self.setup()

    def sort(self):
        self.bookshelf.sort()
        self.setup()

    def toKindle(self):
        if self.isTransfering is True:
            return
        else:
            self.isTransfering = True
            self.transferThread = threading.Thread(target=self.__transfer__, daemon=True)
            self.transferThread.run()

    def setup(self):
        self.__setGui__()
        self.__setButtons__()

    def __setGui__(self):
        self.gui.setLabelText('title', "Ebook Handler")
        self.gui.setLabelText('bookshelf_count', "Bookshelf: " + str(self.bookshelf.numberOfBooksInShelf()))
        self.gui.setLabelText('connected', self.findKindle())
        self.gui.setLabelText('stored_count', "To Move: " + str(self.bookshelf.numberOfBooksToMove()))

    def __setButtons__(self):
        self.gui.getGuiItem('sort').on_press = self.sort
        self.gui.getGuiItem('to_kindle').disabled = self.kindleDisabled
        self.gui.getGuiItem('to_kindle').on_press = self.toKindle

    def __setThreads__(self):
        self.pollThread = threading.Thread(target=self.pollDevice, daemon=True)
        self.pollThread.start()

    def __transfer__(self):
        print("Transfer Initiated")
        self.bookshelf.toKindle()
        print("Transfer Complete")
        self.isTransfering = False


class EbookHandlerApp(App):
    title = 'Ebook Handler'

    def build(self):
        Window.clearcolor = get_color_from_hex("#262626")
        Window.size = (WIDTH, HEIGHT)
        return EbookHandler()


if __name__ == '__main__':
    EbookHandlerApp().run()