import os
import sys
import json
import logging
import logging.config
from argparse import ArgumentParser

from phonesis.train import Trainer
from phonesis.impl import Parser, Tokenizer
from phonesis.constants import DEFAULT_CONS, DEFAULT_VOWS

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('phonesis')


def run_letter_parser():
    word = "each".lower()
    syparse = Parser()
    tokens = syparse(word)
    print(tokens)


def run_eg():
    """Main function
    """
    text = """
    Each Machine Learning Crash Course module is self-contained,
    so if you have prior experience in machine learning, you can skip directly
    to the topics you want to learn. If you're new to machine learning,
    we recommend completing modules in the order below.
    """
    print(text)
    trainer = Trainer([text], DEFAULT_CONS, DEFAULT_VOWS)
    trainer.run()
    model = trainer.get_model()
    model.save('sybok_model.json')
    model.load('sybok_model.json')
    print("vocab:", model.vocab)
    print(model([text]))


def retrieve_alphabet(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        data = json.load(file)
        if ('consonants' not in data) or ('vowels' not in data):
            return
        consonants = data['consonants']
        vowels = data['vowels']
        return consonants, vowels


def read_text_file(file_path):
    file_size = os.path.getsize(file_path)
    size_read = 0
    print("INFO: file size:", file_size)
    with open(file_path, mode='r', encoding='utf-8') as file:
        while (line := file.readline()):
            size_read += len(line)
            line_split = line.split()
            print(f"{100 * (size_read / file_size):5.2f}", f"line: {line}")
            if len(line_split) < 1:
                continue
            yield line_split[0]


def train():
    """
    Training function
    """
    parser = ArgumentParser(prog="Phonesis model training")
    parser.add_argument(
        '-a', "--alphabet", type=str,
        help="Provide a JSON file that provides the alphabet"
    )
    parser.add_argument(
        '-d', "--dictionary", type=str,
        help=(
            "Provide the dictionary as text file that contents"
            " the words of the language."
        )
    )
    parser.add_argument(
        '-o', '--output', type=str, default="output.json",
        help="Provide the output file path in which we will save the tokens."
    )
    args = parser.parse_args()
    alphabet_file = args.alphabet
    dictionary_file = args.dictionary
    output_file = args.output

    if not alphabet_file:
        print("ERRO: No alphabet file provided.")
        print("INFO: Please, provide alphabet json file "
              "separated in consonants and vowels.")
        print("INFO: Eg: {\"consonants\":[..], \"vowels\":[]}")
        exit(0)
    if not dictionary_file:
        print("ERRO: No dictionary of language provided.")
        print("INFO: Please, provide a text (.txt) file "
              "that contains the words list of the language.")
        exit(0)

    returned = retrieve_alphabet(alphabet_file)
    if not returned:
        print("The content formatting of alphabet file is not supported.")
        exit(1)
    consonants = returned[0]
    vowels = returned[1]
    dataset = read_text_file(dictionary_file)

    # Running training process:
    trainer = Trainer(dataset, consonants, vowels)
    n_vocab = trainer.run()
    model = trainer.get_model()
    model.save(output_file)
    print("SUCC: Training done successfully!")
    print(f"INFO: The size of vocab: {n_vocab}")


def inference():
    argv = sys.argv[1:]
    if len(argv) <= 0:
        print("ERRO: No model file provided.")
        print("INFO: Please, provide model json file. "
              "separated in consonants, vowels and vocab.")
        print("INFO: Eg: {\"consonants\":[..], \"vowels\":[], \"vocab\":[]}")
        sys.exit(0)
    model_fp = argv[0]
    model = Tokenizer()
    model.load(model_fp)
    model.raises_except = True
    print("vocab size:", len(model.vocab))
    while True:
        text = input(">_ ")
        if not text:
            continue
        res = model([text])
        print("INFO: seq:", res[0][0])
        print("INFO: ind:", res[0][1])


if __name__ == '__main__':
    try:
        # run_letter_parser()
        inference()
    except KeyboardInterrupt:
        print("\033[91mCanceled by user!\033[0m")
        sys.exit(125)
