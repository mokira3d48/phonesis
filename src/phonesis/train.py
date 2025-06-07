import logging
from .impl import Parser, Tokenizer, preprocess
from .utils.pgit import PBM, ProgressBar

logger = logging.getLogger(__name__)


class Trainer:
    """
    Training process

    :arg dataset: The dataset containing the words of the langauge
    :arg consonants: The list of consonants used to build the words
      of the language
    :arg vowels: The list of vowels used to build the words of the language
    :arg vocab: The set of existing token

    :type dataset: typing.Iterable
    :type consonants: `list` of `str`
    :type vowels: `list` of `str`
    :type vocab: `list` of `str`
    """
    def __init__(self, dataset, consonants, vowels, vocab=None):
        self.dataset = dataset
        self.consonants = consonants
        self.vowels = vowels
        self.vocab = vocab if vocab else []
        self.parse = Parser(consonants, vowels)
        self._model = None

        # self.pbm = PBM()
        # self.pbar = ProgressBar()
        # self.pbar.bins = 100
        # self.pbar.name = "progressbar"
        # self.pbar.bchr = '='
        # self.pbar.pchr = '>'
        # self.pbar.empt = '.'
        # self.pbar.lchr = '['
        # self.pbar.rchr = ']'
        # self.pbm.append(self.pbar)
        # self.pbar.length = len(self.dataset)

    def get_model(self):
        if not self._model:
            self._model = Tokenizer(self.vocab, self.consonants, self.vowels)
        return self._model

    def run(self):
        new_tokens = []
        for sample in self.dataset:
            words = preprocess(sample, self.consonants, self.vowels)

            for word in words:
                if not word:
                    continue
                tokens = self.parse(word)
                for token in tokens:
                    if token in self.vocab:
                        continue
                    if token in new_tokens:
                        continue
                    new_tokens.append(token)
                # self.pbar.step(1)

        new_tokens.sort()
        self.vocab.extend(new_tokens)

        vocab_size = len(new_tokens)
        logger.info(
            f"Training process is done in " + "{progressbar_duration}."
            f" {vocab_size} tokens are found."
        )
        return vocab_size
