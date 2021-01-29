# RAW-C

GitHub page for the RAW-C dataset: Relatedness of Ambiguous Words, in Context.

## Data

There are several data files.

Most relevant is [`data/stims/raw-c.csv`](https://github.com/seantrott/raw-c/blob/main/data/processed/raw-c.csv): the complete set of sentence pairs in the final RAW-C dataset. The most important columns (for most purposes) are:

- `word` 
- `sentence1` and `sentence2`: the sentence pair being contrasted  
- `same`: whether the target word has the same or different meaning across the sentence pair  
- `ambiguity_type`: whether the different-sense use is Polysemy or Homonymy  
- `mean_relatedness`: the mean relatedness judgment across human participants  
- `distance_bert`: the cosine distance between BERT's representation of the target word  
- `distance_elmo`: the cosine distance between ELMo's representation of the target word  

This file also contains information about the number of annotators who rated each sentence pair (`count`), as well as the variance across those judgments (`sd_relatedness`). 

We also include another version of this file, which does not contain the human relatedness judgments, but does have the BERT/ELMo norms (`data/processed/stims_with_nlm_distances.csv`). This can be used to run the `nlm_analysis.Rmd` file.

Finally, we include the original stimuli file (`data/stims/stimuli.csv`).

## Language modeling

The file `src/modeling/get_distances.py` can be used to run each sentence pair through BERT and ELMo, and extract the cosine distance from the contextualized representations:

```
python src/modeling/get_distances.py
```

Note that this script requires the [`bert-embedding` package](https://pypi.org/project/bert-embedding/), as well as the [`allennlp` package](https://github.com/allenai/allennlp).

## Analysis scripts

We include the analysis file for original stimuli, using BERT and ELMo (`data/src/analysis/nlm_analysis.html`). This can be rerun by "knitting" the .Rmd file (`data/src/analysis/nlm_analysis.Rmd`).  

We also include the analysis file for analyzing the individual trial data (`data/src/analysis/norming_analysis.html`). Note that this file also performs the analyses in Section 5.3 of the paper (the language model evaluations). The individual trial data is available upon request (sttrott@ucsd.edu). 