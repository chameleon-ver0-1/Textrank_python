# -*- coding: utf-8 -*-

import re

from konlpy.tag import Komoran


class RawSentence:
    def __init__(self, textIter):
        if type(textIter) == str:
            self.textIter = textIter.split('\n')
        else:
            self.textIter = textIter

        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in self.textIter:
            ch = self.rgxSplitter.split(line)

            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s:
                    continue

                yield s


class RawSentenceReader:
    def __init__(self, filepath):

        self.filepath = filepath
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in open(self.filepath, encoding='utf-8'):
            ch = self.rgxSplitter.split(line)

            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s:
                    continue

                yield s


class RawTagger:
    def __init__(self, textIter, tagger=None):
        if tagger:
            self.tagger = tagger
        else:
            self.tagger = Komoran()

        if type(textIter) == str:
            self.textIter = textIter.split('\n')
        else:
            self.textIter = textIter

        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in self.textIter:
            ch = self.rgxSplitter.split(line)

            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s:
                    continue

                yield self.tagger.pos(s)


class RawTaggerReader:
    def __init__(self, filepath, tagger=None):
        if tagger:
            self.tagger = tagger
        else:
            self.tagger = Komoran()

        self.filepath = filepath
        self.rgxSplitter = re.compile('([.!?:](?:["\']|(?![0-9])))')

    def __iter__(self):
        for line in open(self.filepath, encoding='utf-8'):
            ch = self.rgxSplitter.split(line)

            for s in map(lambda a, b: a + b, ch[::2], ch[1::2]):
                if not s:
                    continue

                yield self.tagger.pos(s)
