import polars as pl

df = pl.read_csv("led_zeppelin.csv", try_parse_dates=True)

df = df.with_columns(
    df.get_column("album").str.to_lowercase(),
    df.get_column("track").str.to_lowercase(),
    (
        df.get_column("lyrics")
        .str.replace_all(r'^\d+ Contributor.*\n?', '')
        .str.replace_all(r'\[.*\]', '')
        .str.replace_all('\n', ' ')
        .str.replace_all('\u200a', ' ')
        .str.replace_all('\u205f', ' ')
        .str.replace_all('\u2005', ' ')
        .str.replace_all('  ', ' ')
        .str.strip_chars()
        .str.to_lowercase()
    )
)

df.write_csv("led_zeppelin_cleaned.csv")
