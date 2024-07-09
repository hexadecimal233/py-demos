# 用落雪音乐导出歌单CSV然后处理数据

import csv

artist_count_map = {}

with open("my_fav.csv") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        artists = row["艺术家"].split("、")
        for artist in artists:
            artist_count_map[artist] = artist_count_map.get(artist, 0) + 1

artist_count_map = sorted(artist_count_map.items(), key=lambda x: x[1], reverse=True)

#for e in range(len(artist_count_map)):
#    print("Top{}：{} {}".format(e + 1, artist_count_map[e][0], artist_count_map[e][1]))

with open("my_fav_tops.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(("歌手名", "次数"))
    writer.writerows(artist_count_map)

#for artist, count in artist_count_map:
#    print(f"{artist},{count},")