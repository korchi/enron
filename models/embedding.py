import json
import logging
from configparser import ConfigParser
from typing import Dict

import numpy as np
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from models.base_model import Model


class EmbeddingModel(Model):
    def __init__(self, cfg: ConfigParser):
        self.cfg = cfg
        self.etalons = json.loads(cfg.get('ETALONS', 'sentences'))
        self.threshold = cfg.getfloat('MODEL', 'threshold')

        self._load_model()
        self.etalons_embedded = self._embed(self.etalons)

    def _load_model(self):
        self.model_name = self.cfg.get('MODEL', 'name')

        logging.info(f'Loading {self.model_name}')
        print(f'Loading {self.model_name}')
        self.embedder = SentenceTransformer(self.model_name)

        self.sentence_splitter_name = self.cfg.get('SENTENCER', 'name')
        self.nlp = spacy.load(self.sentence_splitter_name)

        self.is_model_loaded = True

    def predict(self, text: str) -> Dict:

        if not isinstance(text, str):
            return None

        logging.info('Splitting sentences...')
        sentences = self._split_to_sentences(text)
        logging.info(f'{len(sentences)} sentences.')
        logging.info(f'Embeding them...')
        embeddings = self._embed(sentences)
        logging.info(f'Done.')

        result = {}

        for etalon, etalon_embedding in zip(self.etalons, self.etalons_embedded):
            dist = cosine_similarity(embeddings, [etalon_embedding]).T[0]

            logging.info(f'dist={dist}')
            ind = np.where(dist > self.threshold)[0]
            logging.warning(ind)

            logging.debug(f'ind={ind}')

            if len(ind) > 0:
                for i in ind:
                    etalon_results = result.get(etalon, [])
                    etalon_results.append({'distance': str(dist[i]),
                                           'sentence': sentences[i]})

                    result[etalon] = etalon_results
                    logging.info(f'etalon "{etalon}": ({dist[i]}, {sentences[i]}')

            result['suspicious'] = any([e in result for e in self.etalons])
        return result

    def _embed(self, corpus):
        corpus_embedding = []
        for text in corpus:
            encoding = self.embedder.encode(text)
            corpus_embedding.append(encoding)

        return corpus_embedding

    def _split_to_sentences(self, text):
        return [str(i) for i in self.nlp(text).sents]
