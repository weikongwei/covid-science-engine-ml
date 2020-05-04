# covid-science-engine-ml

## Dataloader usage
```
c19_loader = CORD19_dataloader(paper_subsets=["commerical", "non-commercial"])
c19_loader[98]  # returns an unprocessed dictionary containing the metadata and json index.

```

Arguments:
`paper_subsets` options: ["commerical", "non-commercial", "custom", "biorxiv/medrxiv", "arxiv"] or "all"
 Select which dataset you are looking for. See https://www.semanticscholar.org/cord19/download for more details


# Todo:
## Dataloader
- [x] Skeleon
- [x] Download indexes
- [ ] Filters by metadata to data into memory
- [ ] output text preprocessors and selectors

# Relevant literature
* https://arxiv.org/pdf/2004.10706.pdf
* https://huggingface.co/deepset/covid_bert_base
