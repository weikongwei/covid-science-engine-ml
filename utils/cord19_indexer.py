import os
import glob
import json
import tqdm

import pandas as pd

class CORD19_indexer:
    '''
    Helper class to parse the JSON index files.
    Parameters:
    -----------
    data_path: str, default: "data"
        Location to save the dataset

    filters: TODO
    '''
    def __init__(self, data_path, filters=None):
        self.data_path = data_path
        self.metadata = self.load_metadata()
        self.paper_paths = self._filter_paper_paths(filters)
        
    def load_metadata(self):
        metadata_path = os.path.join(self.data_path, "metadata.csv")
        assert os.path.exists(metadata_path), "metadata.csv does not exist in {}".format(self.data_path)
        return pd.read_csv(metadata_path)

    def _filter_paper_paths(self, filters):
        print("Filtering papers")
        glob_path = os.path.join(self.data_path, "**/*.json")
        if filters == None:
            return glob.glob(glob_path, recursive=True)

        output_paths = []
        # Make the filtering processing multithreaded
        for index_file in tqdm.tqdm(glob.glob(glob_path, recursive=True)):
            with open(index_file, "r") as f:
                index = json.load(f)
                metadata = self.match_metadata(index)
                
            # TODO: include filters based on metadata here
            output_paths.append(index_file)
        return output_paths
                
    def match_metadata(self, index):
        paper_id = index["paper_id"]

        column_indexes = ["pmcid", "sha"]
        # Try to load metadata from different columns
        for column in column_indexes:
            metadata = self.metadata[self.metadata[column]==paper_id]
            
            if len(metadata) > 0:
                return metadata.iloc[0].to_dict()

        # Last resort, search through sha column
        for _, value in self.metadata["sha"].iteritems():
            if isinstance(value, str): # Check if value is nan
                if paper_id in value:
                    return self.metadata.iloc[index].to_dict()

    def __len__(self):
        return len(self.paper_paths)

    def __getitem__(self, index):
        index_file = self.paper_paths[index]
        with open(index_file, "r") as f:
            index = json.load(f)
            metadata = self.match_metadata(index)

        output = {"metadata": metadata, "index": index}
        return output
