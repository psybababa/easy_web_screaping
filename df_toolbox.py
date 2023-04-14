#こっちはデータの前処理がメイン。
import matplotlib.pyplot as plt
import neologdn
import numpy as np
import pandas as pd
import spacy
from spacymoji import Emoji
import MeCab
import sudachipy as sp

class Convert:
    def __init__(self):
        self.files = [
            {
                "fname": "comments",
                "encoding": "utf_8_sig",
                "mode": "a"
            },
            {
                "fname": "threads",
                "encoding": "utf_8_sig",
                "mode": "a"
            },
            {"fname": "titles",
             "encoding": "utf_8_sig",
             "mode": "a"
            },
        ]

    def convfile(self, finfo):
        df = pd.read_pickle(f"./data/{finfo["fname"]}.pkl")
        df.to_csv(f"./data/{finfo["fname"]}.csv", encoding=finfo["encoding"], mode=finfo["mode"])

    def convall(self):
        for finfo in self.files:
            self.convfile(finfo)

class process:
    def __init__(self):
        pass
    
    def cleantxt(self,txt):
        pass    
    
    def deldup(self,finfo):
        df = pd.read_csv(f"./data/{finfo["fname"]}")
    
    def tokenize(self,txt):
        tokenizer = sp.Dictionary.create()
        tokens = tokenizer.tokenize(txt)
        return [token.surface() for token in tokens]
        

class visualize:
    