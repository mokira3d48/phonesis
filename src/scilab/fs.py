import os
import json


class FileHandler:
    """
    File handler

    :param model: The instance of Tokenizer model
    :param file_path: The path to file where we want to save tokenizer data

    :type model: scilab.tokenizer.Tokenizer
    :type file_path: `str`
    """
    def __init__(self, model, file_path):
        assert file_path, "The file path is not defined."
        self.model = model
        self.file_path = file_path

    def save(self):
        """
        Method to save data of Tokenizer instance into file_path
        """
        with open(self.file_path, mode='w', encoding='utf-8') as f:
            consonants = []
            vowels = []
            vocab = []
            if self.model.consonants:
                consonants = self.model.consonants
            if self.model.vowels:
                vowels = self.model.vowels
            if self.model.vocab:
                vocab = self.model.vocab
            data = dict(consonants=consonants, vowels=vowels, vocab=vocab)
            jsonify = json.dumps(data, indent=2)
            f.write(jsonify)

    def load(self):
        """
        Method to load data of tokenizer model from file_path specified

        :rtype: scilab.tokenizer.Tokenizer
        """
        if not os.path.isfile(self.file_path):
            raise FileNotFoundError(f"No such model file at {self.file_path}")

        with open(self.file_path, mode='r', encoding='utf-8') as f:
            data = json.load(f)
            self.model.consonants = data['consonants']
            self.model.vowels = data['vowels']
            self.model.vocab = data['vocab']
            return self.model
