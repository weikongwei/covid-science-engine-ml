import os

from utils.cord19_downloader import CORD19_downloader
from utils.cord19_indexer import CORD19_indexer

class CORD19_dataloader:
    '''
    Data loader for the CORD-19 dataset. 
    Parameters:
    -----------
    paper_subsets: [] or "str", default: "all", options: ["commerical", "non-commercial", "custom",
                                                          "biorxiv/medrxiv", "arxiv"] or "all"
                   
        Select which dataset you are looking for. See https://www.semanticscholar.org/cord19/download
        for more details
    
    data_path: str, default: "data"
        Location to save the dataset
    '''

    # TODO: - filters for loading data into memory,
    #       - preprocessors
    #       - selecting what data to output
    #       - quick load option

    def __init__(self, paper_subsets="all", data_path="data"):
        self.c19_downloader = CORD19_downloader(paper_subsets, data_path)
        self.c19_indexer = CORD19_indexer(data_path)
        
    def __len__(self):
        return len(self.c19_indexer)

    def __getitem__(self, index):
        return self.c19_indexer[index]
        
