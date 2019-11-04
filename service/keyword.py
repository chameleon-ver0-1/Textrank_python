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
            # TODO: 예지 수정 --> 배열접근위해 문자열형식에서 원래 형식으로 바꿈
            abstracted_keywords[k] = kw[k]

        return abstracted_keywords
