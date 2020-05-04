import os
import numpy as np
import requests
from tqdm import tqdm
import tarfile

class CORD19_downloader:
    '''
    Helper class to download paper indexes from the CORD-19 dataset. 
    The paper indexes are JSON files that contains information about the papers

    Parameters:
    ----------
    paper_subsets: [] or "str", default: "all", options: ["commerical", "non-commercial", "custom",
                                                          "biorxiv/medrxiv", "arxiv"] or "all"
                   
        Select which dataset you are looking for. See https://www.semanticscholar.org/cord19/download
        for more details
    
    data_path: str, default: "data"
        Location to save the dataset
    '''
    CORD_19_BASE_URL = "https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/"
    SUBSET_RELATIVE_PATHS = {"commerical": "comm_use_subset",
                             "non-commercial": "noncomm_use_subset",
                             "custom": "custom_license",
                             "biorxiv/medrxiv": "biorxiv_medrxiv", 
                             "arxiv": "arxiv"}
    METADATA_PATH = "metadata.csv"

    def __init__(self, paper_subsets="all", data_path="data"):

        # Check if subsets are valid
        if isinstance(paper_subsets, str):
            if paper_subsets == "all":
                paper_subsets = ["commerical", "non-commercial", "custom", "biorxiv/medrxiv", "arxiv"]

        all_subset_names = [a for a in self.SUBSET_RELATIVE_PATHS.keys()]
        subsets_exists = np.in1d(paper_subsets, all_subset_names)
        assert subsets_exists.all(), "{} is not a valid subset".format(
            np.array(paper_subsets)[np.logical_not(subsets_exists)])

        # Check datapath
        self.data_path = data_path
        if not os.path.exists(data_path):
            os.mkdir(data_path)

        # Download the subsets
        for paper_subset in paper_subsets:
            if not self.check_does_data_exist(paper_subset):
                if not self.check_does_tar_exist(paper_subset):
                    self.download_index_tar(paper_subset)
                self.extract_index_tar(paper_subset)

        # Download the metadata
        self.download_metadata()

    def check_does_data_exist(self, paper_subset):
        dir_name = self.SUBSET_RELATIVE_PATHS[paper_subset]
        target_path = os.path.join(self.data_path, dir_name)
        return os.path.exists(target_path)
        
    def check_does_tar_exist(self, paper_subset):
        tar_name = self.SUBSET_RELATIVE_PATHS[paper_subset] + ".tar.gz"
        target_path = os.path.join(self.data_path, tar_name)
        return os.path.exists(target_path)
        
    def download_index_tar(self, paper_subset):
        tar_name = self.SUBSET_RELATIVE_PATHS[paper_subset] + ".tar.gz"
        url = os.path.join(self.CORD_19_BASE_URL, tar_name)
        target_path = os.path.join(self.data_path, tar_name)
        print("Downloading subset: {} from {}".format(paper_subset, url))
        self._download(url, target_path)

    def download_metadata(self):
        metadata_url = os.path.join(self.CORD_19_BASE_URL, self.METADATA_PATH)
        metadata_target_path = os.path.join(self.data_path, self.METADATA_PATH)

        if os.path.exists(metadata_target_path):
            return
        
        print("Downloading the meta data")
        self._download(metadata_url, metadata_target_path)

    def extract_index_tar(self, paper_subset):
        tar_name = self.SUBSET_RELATIVE_PATHS[paper_subset] + ".tar.gz"
        tar_path = os.path.join(self.data_path, tar_name)
        print("Extracting {}".format(tar_path))

        tf = tarfile.open(tar_path)
        tf.extractall(path=self.data_path)

    def _download(self, url, target_path):
        response = requests.get(url, stream=True)

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        t = tqdm(total=total_size, unit='iB', unit_scale=True)
        
        with open(target_path, 'wb') as f:
            for data in response.iter_content(block_size):
                t.update(len(data))
                f.write(data)
        t.close()
