import logging
import logging.config


logging.config.fileConfig('logging.conf')
logger = logging.getLogger('phonesis')


def main():
    """
    Main function to run execution example
    """
    print("Running phonesis module for NLP tokenization.")


if __name__ == '__main__':
    main()
