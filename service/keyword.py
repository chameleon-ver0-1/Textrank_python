from common.textrank import TextRank
from common.reader import RawTaggerReader


class Keyword:
    _stop_word = set()

    def __init__(self, filepath: str, stop_word: list):
        self._filepath = filepath
        self._stop_word.add(stop_word)

    def run(self) -> dict:
        tr = TextRank(window=5, coef=1)

        tr.load(RawTaggerReader(self._filepath),
                lambda w: w not in self._stop_word and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))

        tr.build()
        kw = tr.extract(0.2)

        abstracted_keywords = {}

        for k in sorted(kw, key=kw.get, reverse=True):
            abstracted_keywords[f'{k}'] = f'{kw[k]}'

        return abstracted_keywords
