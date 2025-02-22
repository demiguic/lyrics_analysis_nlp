import spacy
import polars as pl

nlp = spacy.load('en_core_web_sm')  # Loading default model


def tokens(text: str) -> int:
    """Number of tokens in the text"""
    doc = nlp(text)
    return len([t.text for t in doc if not t.is_punct])


def types(text: str) -> int:
    """Number of unique elements (types) in the text"""
    doc = nlp(text)
    return len(set([t.text for t in doc if not t.is_punct]))


def ttr(cols) -> float:
    """
    Computes the Type-Token Ratio (TTR) for a given text.
    TTR is a measure of lexical diversity in a given text.
    TTR = (Number of unique words) / (Total number of words)
    """
    types = cols.get('types', 0)
    tokens = cols.get('tokens', 0)
    return (types / tokens) * 100 if tokens not in (None, 0) else 0.0


def lemma_ratio(cols) -> float:
    """
    X = (Number of unique lemmas) / (Total number of words)
    """
    lemmas = cols.get('lemmas', 0)
    types = cols.get('types', 0)
    return (lemmas / types) * 100 if types not in (None, 0) else 0.0


def lemmas(text: str) -> float:
    doc = nlp(text)
    return len(set([t.lemma_ for t in doc if not t.is_punct]))


df = pl.read_csv('led_zeppelin_cleaned.csv')

new_df = df.with_columns(
    (
        pl.col("lyrics")
        .alias("tokens")
        .map_elements(tokens, return_dtype=int)
    ),
    (
        pl.col("lyrics")
        .alias("types")
        .map_elements(types, return_dtype=int)
    ),
    (
        pl.col("lyrics")
        .alias("lemmas")
        .map_elements(lemmas, return_dtype=int)
    )
).with_columns(
    (
        pl.struct(
            ['types', 'tokens']
        )
        .alias('ttr')
        .map_elements(ttr, return_dtype=float)
    ),
    (
        pl.struct(
            ['lemmas', 'types']
        )
        .alias('lemma_ratio')
        .map_elements(lemma_ratio, return_dtype=float)
    )
)

new_df.write_csv('led_zeppelin_stats.csv')