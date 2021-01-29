"""Get cosine distances with ELMo and BERT.

ELMo package: allennlp elmo_embedder

BERT package: https://github.com/negedng/bert-embedding#egg=bert_embedding
"""


import itertools

import pandas as pd
import seaborn as sns

from scipy.spatial.distance import cosine
from tqdm import tqdm



### PATHS
STIMULI_PATH = "data/stims/stimuli.csv"
SAVE_PATH = "data/processed/stims_with_nlm_distances.csv"
VERSIONS = ['M1_a', 'M1_b', 'M2_a', 'M2_b']

### Read in stims
df_stims = pd.read_csv(STIMULI_PATH)
df_stims.head(5)
print("{X} words with 4 sentence pairs each.".format(X=len(df_stims)))


### Load ELMo stuff
from allennlp.commands.elmo import ElmoEmbedder
elmo = ElmoEmbedder(
    options_file='https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_options.json', 
    weight_file='https://s3-us-west-2.amazonaws.com/allennlp/models/elmo/2x4096_512_2048cnn_2xhighway_5.5B/elmo_2x4096_512_2048cnn_2xhighway_5.5B_weights.hdf5'
)

### Load BERT stuff
from bert_embedding import BertEmbedding
bert = BertEmbedding()


## Helper functions
def clean_sentence(sentence):
    return sentence.lower().replace(".", "").split()

def get_ELMo_embedding(sentence, target_index):
    """Preprocess sentence string and produce elmo embedding."""
    sentence_cleaned = sentence.lower().replace(".", "").split()
    return elmo.embed_sentence(sentence_cleaned)[2][target_index]

def get_BERT_embedding(sentence, target_index):
    """Preprocess sentence string and produce elmo embedding."""
    sentence_cleaned = [sentence]
    result = bert(sentence_cleaned)
    return result[0][1][target_index]



comparisons = []

with tqdm(total=len(df_stims)*6) as progress_bar:
    for index, row in df_stims.iterrows():

        target_word = row['String']

        for v1, v2 in itertools.combinations(VERSIONS, 2):

            version = '{v1}_{v2}'.format(v1=v1, v2=v2)
            same = v1[0:2] == v2[0:2]

            # Two versions
            ex1 = row[v1]
            ex2 = row[v2]

            # Cleaned
            ex1_cleaned = clean_sentence(ex1)
            ex2_cleaned = clean_sentence(ex2)

            # Indices
            ex1_index = ex1_cleaned.index(target_word)
            ex2_index = ex2_cleaned.index(target_word)

            # BERT
            b1 = get_BERT_embedding(ex1, ex1_index)
            b2 = get_BERT_embedding(ex2, ex2_index)

            ## TODO: ELMo

            # ELMo
            e1 = get_ELMo_embedding(ex1, ex1_index)
            e2 = get_ELMo_embedding(ex2, ex2_index)

            comparisons.append({
                'string': row['String'],
                'distance_bert': cosine(b1, b2),
                'distance_elmo': cosine(e1, e2),
                'same': same,
                'ambiguity_type_mw': row['Different_entries_MW'],
                'ambiguity_type_oed': row['Different_entries_OED'],
                'ambiguity_type': row['Ambiguity_Type'],
                'different_frame': row['Different_frame'],
                'overlap': row['Original Condition'],
                'Class': row['Class'],
                'version': version,
                'source': row['Source'],
                'word': row['Word']
                })

            progress_bar.update(1)


            
## Create dataframe
df_distances = pd.DataFrame(comparisons)

## Save data
df_distances.to_csv(SAVE_PATH)
