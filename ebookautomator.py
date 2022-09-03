#!/usr/bin/python3
import sys
import os
import platform
from pathlib import Path
from shutil import copyfile


class Defaults:
    STORE_PATH = "bookshelf/"
    SEARCH_PATH = "Downloads/"
    FILE_SIZE = 14
    CONFIG = "config.conf"


defaults = Defaults()


class Container:
    def setupEnvironment(self):
        os.chdir(Path.home())
        if os.path.exists(defaults.STORE_PATH):
            print("environment already setup")
            return
        else:
            os.mkdir(Defaults().STORE_PATH)
            config = open(defaults.STORE_PATH + defaults.CONFIG, "a")
            config.write("store_path {}\n".format(defaults.STORE_PATH))
            config.write("search_path {}\n".format(defaults.SEARCH_PATH))
            config.write("file_size {}\n".format(str(defaults.FILE_SIZE)))
            config.close()


class Librarian:
    def __init__(self):
        os.chdir(Path.home())

    def list(self):
        os.chdir(Path.home())
        files = os.listdir(defaults.STORE_PATH)
        for file in files:
            if file.__contains__(".conf"):
                continue
            print(file.split(".")[0])

    def numberOfBooksInPath(self, path):
        files = os.listdir(path)
        bookCount = 0
        for file in files:
            if self.__validateFileType__(file):
                bookCount += 1
        return bookCount

    def sort(self):
        files = os.listdir(defaults.SEARCH_PATH)
        for file in files:
            if file.__contains__(".mobi"):
                self.__storeFile__(file)
            if file.__contains__(".pdf"):
                if self.__validateFileSize__(file) > defaults.FILE_SIZE:
                    self.__storeFile__(file)
            if file.__contains__(".epub"):
                self.__storeFile__(file)

    def copyToKindle(self):
        if platform.system().lower() == "darwin":
            self.__macosCopyToKindle__()
        else:
            print("Your platform is currently not supported")

    def __macosCopyToKindle__(self):
        # List all books that are already stored on kindle
        kindlePath = "/Volumes/Kindle/documents/"
        if not os.path.isdir(kindlePath):
            print("kindle is not detected")
            return

        shouldCopy = True
        kindleBooks = list()
        self.__loopAndStore__(kindlePath, kindleBooks, shouldCopy)
        files = os.listdir(defaults.STORE_PATH)
        for rawFile in files:
            file = rawFile.split(".")[0]
            if os.path.isdir(defaults.STORE_PATH + rawFile):
                continue
            if file == "config":
                continue
            if kindleBooks.__contains__(file):
                continue
            print("is copying: {}".format(file))
            copyfile(defaults.STORE_PATH + rawFile, kindlePath + rawFile)

    def __loopAndStore__(self, path, dest, shouldCopy):
        files = os.listdir(path)
        for rawFile in files:
            file = rawFile.split(".")[0]
            if os.path.isdir(path + rawFile):
                continue
            if file == "config":
                continue
            if dest.__contains__(file):
                continue
            if shouldCopy:
                dest.append(file)

    def __validateFileSize__(self, file):
        fileSizeInBytes = os.path.getsize(defaults.SEARCH_PATH + file)
        return fileSizeInBytes / (1024*1024)

    def __validateFileType__(self, file):
        valid = False
        if file.__contains__(".mobi"):
            valid = True
        elif file.__contains__(".pdf"):
            #if self.__validateFileSize__(file) > defaults.FILE_SIZE:
            valid = True
        elif file.__contains__(".epub"):
            valid = True
        return valid

    def __storeFile__(self, file):
        origin = defaults.SEARCH_PATH + file
        destination = defaults.STORE_PATH + file
        os.rename(origin, destination)


class Bookshelf:
    def __init__(self):
        self.container = Container()
        self.librarian = Librarian()

    def list(self):
        self.librarian.list()

    def setup(self):
        self.container.setupEnvironment()

    def sort(self):
        self.librarian.sort()

    def toKindle(self):
        self.librarian.copyToKindle()

    def numberOfBooksInShelf(self):
        return self.librarian.numberOfBooksInPath(defaults.STORE_PATH)

    def numberOfBooksToMove(self):
        return self.librarian.numberOfBooksInPath(defaults.SEARCH_PATH)


def __main__(argv):
    container = Container()
    librarian = Librarian()

    for cmdL in argv:
        cmdLower = cmdL.lower()
        if cmdLower == "-l":
            librarian.list()
        if cmdLower == "-s":
            librarian.sort()
        if cmdLower == "-c":
            container.setupEnvironment()
        if cmdLower == "-ctk":
            librarian.copyToKindle()


__main__(sys.argv[1:])