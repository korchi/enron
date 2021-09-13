import os
from configparser import ConfigParser

import pytest

from models.embedding import EmbeddingModel


@pytest.fixture(scope="module")
def embedder():
    cfg = ConfigParser()
    cfg_path = os.path.join(os.getcwd(), "cfg", "config.ini")
    cfg.read(cfg_path)
    embedder = EmbeddingModel(cfg)
    return embedder


def test_two_non_fraud(embedder):
    results = embedder.predict('Hi Frank. Hello world.')

    assert not results['suspicious']


def test_second_senetence_fraud(embedder):
    sentences = ['We cannot do such fraud.', 'This is definitely fraud!']
    results = embedder.predict(' '.join(sentences))

    assert results['suspicious']
    assert len(results['fraud']) == 2

    for sentence_query, item in zip(sentences, results['fraud']):
        assert sentence_query == item['sentence']
