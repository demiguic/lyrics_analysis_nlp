import matplotlib.pyplot as plt
import polars as pl

df = pl.read_csv('led_zeppelin_stats.csv')

"""
Faixas por disco.
"""
# counter = df.group_by('album').len().sort('len')

# fig, ax = plt.subplots()
# ax.barh(counter['album'], counter['len'])
# plt.show()

"""
Estatísticas por álbum
"""
# for album in df.partition_by('album'):
#     fig, ax = plt.subplots()
#     ax.barh(album['track'], album['tokens'])
#     ax.set_title(f"Álbum: {album['album'][0]}")
#     plt.show()

"""
Estatísticas gerais por target (boxplot).
"""
boxes = {}
target = 'tokens'

for album in df.sort('date').partition_by('album'):
    print(album)