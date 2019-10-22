from konlpy.tag import Komoran
from common.textrank import TextRank
from common.reader import RawSentence


class Summary:
    _stop_word = set()

    def __init__(self, content: str, stop_word: list):
        self._content = content
        self._stop_word.add(stop_word)

    def run(self) -> str:
        tr = TextRank()
        tagger = Komoran()

        tr.load_sentences(RawSentence(self._content),
                          lambda sent: filter(lambda x:
                                              x not in self._stop_word and x[1] in ('NNG', 'NNP', 'VV', 'VA'),
                                              tagger.pos(sent)))

        tr.build()
        ranks = tr.rank()

        # for k in sorted(ranks, key=ranks.get, reverse=True)[:100]:
        #     print("\t".join([str(k), str(ranks[k]), str(tr.dictCount[k])]))

        return tr.summarize(0.3)
