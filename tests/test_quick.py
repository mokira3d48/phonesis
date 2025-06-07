import os
import logging
from phonesis.constants import DEFAULT_CONS, DEFAULT_VOWS
from phonesis.train import Trainer

logger = logging.getLogger(__name__)


def test_all_feature():
    text = """
    Each Machine Learning Crash Course module is self-contained,
    so if you have prior experience in machine learning, you can skip directly
    to the topics you want to learn. If you're new to machine learning,
    we recommend completing modules in the order below.
    """
    logger.info("\n" + text + "\n")
    trainer = Trainer([text], DEFAULT_CONS, DEFAULT_VOWS)
    trainer.run()
    model = trainer.get_model()
    model.save('phsis_model.json')
    model.load('phsis_model.json')

    logger.info("vocab:" + str(model.vocab))
    logger.info(str(model([text])))

    os.remove('phsis_model.json')
