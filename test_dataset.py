from utils.cord19_dataloader import CORD19_dataloader

c19_loader = CORD19_dataloader(paper_subsets=["commerical", "non-commercial"])
item = c19_loader[96]
print(item)
