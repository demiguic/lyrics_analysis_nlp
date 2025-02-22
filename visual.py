import matplotlib.pyplot as plt
import polars as pl

df = pl.read_csv('led_zeppelin_stats.csv')
df_deluxe = df.filter(pl.col('album').str.contains('deluxe edition'))
df_deluxe = df_deluxe.with_columns(
  pl.col('album').str.replace('(deluxe edition)', '', literal=True),
)

"""
Faixas por disco.
"""
# counter = df_deluxe.group_by('album').len().sort('len')

# fig, ax = plt.subplots()
# ax.barh(counter['album'], counter['len'])
# plt.show()

"""
Estatísticas por álbum
"""
for album in df.partition_by('album'):
  fig, ax = plt.subplots()
  ax.barh(album['track'], album['tokens'])
  ax.set_title(f"Álbum: {album['album'][0]}")
  plt.show()
