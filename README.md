# RAW-C

GitHub page for RAW-C (Relatedness of Ambiguous Words——in Context). [[Link to paper](https://aclanthology.org/2021.acl-long.550/)]. 

To cite:

> Trott, S., Bergen, B. (2021). RAW-C: Relatedness of Ambiguous Words––in Context (A New Lexical Resource for English). Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (ACL-IJCNLP 2021).

BibTex:

```bibtex
@inproceedings{trott-bergen-2021-raw,
    title = "{RAW}-{C}: Relatedness of Ambiguous Words in Context (A New Lexical Resource for {E}nglish)",
    author = "Trott, Sean  and
      Bergen, Benjamin",
    editor = "Zong, Chengqing  and
      Xia, Fei  and
      Li, Wenjie  and
      Navigli, Roberto",
    booktitle = "Proceedings of the 59th Annual Meeting of the Association for Computational Linguistics and the 11th International Joint Conference on Natural Language Processing (Volume 1: Long Papers)",
    month = aug,
    year = "2021",
    address = "Online",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.acl-long.550/",
    doi = "10.18653/v1/2021.acl-long.550",
    pages = "7077--7087",
    abstract = "Most words are ambiguous{---}-i.e., they convey distinct meanings in different contexts{---}-and even the meanings of unambiguous words are context-dependent. Both phenomena present a challenge for NLP. Recently, the advent of contextualized word embeddings has led to success on tasks involving lexical ambiguity, such as Word Sense Disambiguation. However, there are few tasks that directly evaluate how well these contextualized embeddings accommodate the more continuous, dynamic nature of word meaning{---}-particularly in a way that matches human intuitions. We introduce RAW-C, a dataset of graded, human relatedness judgments for 112 ambiguous words in context (with 672 sentence pairs total), as well as human estimates of sense dominance. The average inter-annotator agreement (assessed using a leave-one-annotator-out method) was 0.79. We then show that a measure of cosine distance, computed using contextualized embeddings from BERT and ELMo, correlates with human judgments, but that cosine distance also systematically underestimates how similar humans find uses of the same sense of a word to be, and systematically overestimates how similar humans find uses of different-sense homonyms. Finally, we propose a synthesis between psycholinguistic theories of the mental lexicon and computational models of lexical semantics."
```

## Data

There are several data files.

Most relevant is [`data/processed/raw-c.csv`](https://github.com/seantrott/raw-c/blob/main/data/processed/raw-c.csv): the complete set of sentence pairs in the final RAW-C dataset. The most important columns (for most purposes) are:

- `word` 
- `sentence1` and `sentence2`: the sentence pair being contrasted  
- `same`: whether the target word has the same or different meaning across the sentence pair  
- `ambiguity_type`: whether the different-sense use is Polysemy or Homonymy  
- `mean_relatedness`: the mean relatedness judgment across human participants  
- `distance_bert`: the cosine distance between BERT's representation of the target word  
- `distance_elmo`: the cosine distance between ELMo's representation of the target word  
- `string`: the actual target word that occurs in the sentence (e.g., "break" vs. "broke").

This file also contains information about the number of annotators who rated each sentence pair (`count`), as well as the variance across those judgments (`sd_relatedness`). 

We also include another version of this file, which does not contain the human relatedness judgments, but does have the BERT/ELMo norms (`data/processed/stims_with_nlm_distances.csv`). This can be used to run the `nlm_analysis.Rmd` file.

We also include [`data/processed/raw-c_with_dominance.csv`](https://github.com/seantrott/raw-c/blob/main/data/processed/raw-c_with_dominance.csv), which contains all of the same columns as **RAW-C**, with several additions:

- `dominance_sentence2`: mean dominance of `sentence2` relative to `sentence1`.  
- `sd_dominance_sentence2`: standard deviation for dominance judgments of `sentence2` relative to `sentence1`. 

Note that dominance judgments are only included for **different sense** sentence pairs. 

## Language modeling

The file `src/modeling/get_distances.py` can be used to run each sentence pair through BERT and ELMo, and extract the cosine distance from the contextualized representations:

```
python src/modeling/get_distances.py
```

**Note (12/2/2024)**: This script requires the [`bert-embedding` package](https://pypi.org/project/bert-embedding/), as well as the [`allennlp` package](https://github.com/allenai/allennlp). Because the HuggingFace `transformers` package is more widely used, I am working to update this script with the option to run it with `transformers`.

## Analysis scripts

We include the analysis file for original stimuli, using BERT and ELMo (`data/src/analysis/nlm_analysis.html`). This can be rerun by "knitting" the .Rmd file (`data/src/analysis/nlm_analysis.Rmd`).  

We also include the analysis file for analyzing the individual trial data (`data/src/analysis/norming_analysis.html`). Note that this file also performs the analyses in Section 5.3 of the paper (the language model evaluations). The individual trial data is available upon request (sttrott@ucsd.edu). 