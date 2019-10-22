from common.textrank import TextRank
from common.reader import RawTagger


class Keyword:

    def __init__(self, content: str, stop_word: list):
        self._content = content
        self._stop_word = stop_word

    def run(self) -> dict:
        tr = TextRank(window=5, coef=1)

        tr.load(RawTagger(self._content),
                lambda w: w not in self._stop_word and (w[1] in ('NNG', 'NNP', 'VV', 'VA')))

        tr.build()
        kw = tr.extract(0.2)

        abstracted_keywords = {}

        for k in sorted(kw, key=kw.get, reverse=True):
            abstracted_keywords[f'{k}'] = f'{kw[k]}'

        return abstracted_keywords
