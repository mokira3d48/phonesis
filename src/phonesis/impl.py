import re
from .constants import DEFAULT_VOWS, DEFAULT_CONS
from .fs import FileHandler
from .exceptions import UnknownTokenError


def preprocess(x, consonants, vowels):
    """
    Function to preprocess string

    :type x: `str`
    :type consonants: `list` of `str`
    :type vowels: `list` of `str`
    :rtype: `list` of `str`
    """
    data = x.lower()
    data = ''.join([d for d in data \
                    if d in (consonants + vowels + [' '])])
    return re.split(r"[ \n\t\r]", data)


class LetterParse:

    def __init__(self, pattern=None):
        self._pattern = pattern
        self._patterns = []

    def __call__(self, lt_seq, word):
        for pattern in self._patterns:
            res = re.match(pattern, lt_seq)
            if res:
                s, c = res.span()
                extr = lt_seq[s:c]
                sbwd = word[s:c]
                res = re.match(self._pattern, extr)
                s, c = res.span()
                token = sbwd[s:c]
                return token


class Vparse(LetterParse):
    def __init__(self):
        super().__init__()
        self._pattern = re.compile(r'^v+')
        self._patterns = [re.compile(r"^v+$"),
                          re.compile(r"^v+cv")]


class VCparse(LetterParse):
    def __init__(self):
        super().__init__()
        self._pattern = re.compile(r'^v+c')
        self._patterns = [re.compile(r"^v+c$"),
                          re.compile(r"^v+c{2,}")]


class Cparse(LetterParse):
    def __init__(self):
        super().__init__()
        self._pattern = re.compile(r'^c{1}')
        self._patterns = [re.compile(r"^c+$")]


class CVparse(LetterParse):
    def __init__(self):
        super().__init__()
        self._pattern = re.compile(r'^c+v+')
        self._patterns = [re.compile(r"^c+v+$"),
                          re.compile(r"^c+v+cv")]


class CVCparse(LetterParse):
    def __init__(self):
        super().__init__()
        self._pattern = re.compile(r'^c+v+c')
        self._patterns = [re.compile(r'^c+v+c$'),
                          re.compile(r'^c+v+c{2,}')]


class Parser:
    def __init__(self, consonants=DEFAULT_CONS, vowels=DEFAULT_VOWS):
        self.consonants = consonants
        self.vowels = vowels
        self.parsers = [CVCparse(),
                        CVparse(),
                        Cparse(),
                        VCparse(),
                        Vparse()]

    def _get_vow_cons_encoding(self, text):
        letters = ''
        for letter in text:
            if letter in self.consonants:
                letters += 'c'
            elif letter in self.vowels:
                letters += 'v'
        return letters

    def make_parsing(self, word):
        assert word is not None, "Word is None, must be a string."
        letters = self._get_vow_cons_encoding(word)
        tokens = []
        while word:
            for parse in self.parsers:
                token = parse(letters, word)
                if not token:
                    continue
                tokens.append(token)
                word = word[len(token):]
                letters = letters[len(token):]
                break

        tokens.append('#')
        return tokens

    def __call__(self, word):
        return self.make_parsing(word)


class Tokenizer:
    """
    Tokenizer model

    :arg vocab: The list of tokens built with the training process
    :arg consonants: The list of consonants used to build the words
      of the language
    :arg vowels: The list of vowels used to build the words of the language

    :type vocab: typing.List[str]
    :type consonants: typing.List[str]
    :type vowels: typing.List[str]
    """
    def __init__(
        self, vocab=None, consonants=DEFAULT_CONS, vowels=DEFAULT_VOWS
    ):
        self.vocab = vocab
        self.consonants = consonants
        self.vowels = vowels

        self.parse = Parser(consonants, vowels)
        self._file_handler = None
        self._raises_except = False

    @property
    def raises_except(self):
        return self._raises_except

    @raises_except.setter
    def raises_except(self, value):
        self._raises_except = value

    def encode(self, x):
        assert x is not None, "`x` is None. It not is a text."
        words = preprocess(x, self.consonants, self.vowels)
        # print(words)
        indexes = []
        unknowns = {}
        tokens = []

        for pos, word in enumerate(words):
            if not word:
                continue
            tokens = self.parse(word)
            for token in tokens:
                try:
                    index = self.vocab.index(token)
                    indexes.append(index)
                except IndexError:
                    indexes.append(-1)
                    unknowns[word] = pos
                    if self._raises_except:
                        raise UnknownTokenError(
                            f"\"{token}\" is unknown.", token
                        )

        return tokens, indexes, unknowns

    def forward(self, inp):
        out = []
        for s in inp:
            tok = self.encode(s)
            out.append(tok)
        return out

    def load(self, file_path):
        if not self._file_handler:
            self._file_handler = FileHandler(self, file_path)
        self._file_handler.load()
        del self.parse
        self.parse = Parser(self.consonants, self.vowels)

    def save(self, file_path):
        if not self._file_handler:
            self._file_handler = FileHandler(self, file_path)
        self._file_handler.save()

    def __call__(self, inp):
        if not isinstance(inp, list):
            inp = [inp]
        return self.forward(inp)
