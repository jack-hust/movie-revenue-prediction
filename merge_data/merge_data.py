import pandas as pd

'''# Gộp 2 data từ the-numbers và movie-mojo
df_a = pd.read_csv("../mojo/data/all_movie_mojo.csv")
df_b = pd.read_csv("../the-numbers/data/all_the-numbers.csv")

# Thêm cột genres cho df_b với giá trị ""
df_b["genres"] = ""
df_b.drop("international_box_office", axis=1, inplace=True)
df_b.drop("worldwide_box_office", axis=1, inplace=True)

df_a.drop_duplicates(subset=["movie_name"], inplace=True)
df_b.drop_duplicates(subset=["movie_name"], inplace=True)
print(df_a.info())
print(df_b.info())
# Gộp dữ liệu từ hai DataFrame
merged_df = pd.merge(
    df_a,
    df_b,
    on=[
        "movie_name",
    ],
    how="outer",
    suffixes=("_a", "_b"),
)

print(merged_df.info())

# Tạo hàm để lấy giá trị lớn hơn
def choose_greater_value(value_a, value_b):
    if pd.isna(value_a):
        return value_b
    elif pd.isna(value_b):
        return value_a
    else:
        return max(value_a, value_b)


# Áp dụng hàm cho các cột cần so sánh
cols_to_compare = ["month","year","mpaa"]
for col in cols_to_compare:
    merged_df[col] = merged_df.apply(
        lambda row: (
            row[f"{col}_a"] if not pd.isna(row[f"{col}_a"]) else row[f"{col}_b"]
        ),
        axis=1,
    )

# Lấy giá trị lớn hơn cho các cột còn lại
cols_to_get_greater = [
    "budget",
    "runtime",
    "screens",
    "opening_week",
    "domestic_box_office",
]
for col in cols_to_get_greater:
    merged_df[col] = merged_df.apply(
        lambda row: choose_greater_value(row[f"{col}_a"], row[f"{col}_b"]), axis=1
    )

merged_df["genres"] = merged_df["genres_a"]

print(merged_df.info())

# Loại bỏ các cột dư thừa
columns_to_drop = [col for col in merged_df.columns if col.endswith(("_a", "_b"))]
merged_df = merged_df.drop(columns=columns_to_drop, axis=1)

# Lưu kết quả vào file mới
print(merged_df.info())
merged_df.to_csv("merged.csv", index=False)

merged_df.dropna(
    subset=[
        "month",
        "year",
        "runtime",
        "budget",
        "mpaa",
        "screens",
        "opening_week",
        "domestic_box_office",
    ],
    inplace=True,
)
print(merged_df.info())
merged_df = merged_df[merged_df["mpaa"] != "Not"]
merged_df.to_csv("filtered_merged_data.csv", index=False)

print("Tổng hợp dữ liệu thành công và lưu vào file 'merged.csv'.")
'''

# ==================================================================================

# Gộp dữ liệu từ imdb và filtered_merged_data
'''
df_a = pd.read_csv("filtered_merged_data.csv")
df_b = pd.read_csv("../imdb/data/all_data.csv")

print(df_a.info())
print(df_b.info())
# Gộp dữ liệu từ hai DataFrame
merged_df = pd.merge(
    df_a,
    df_b,
    on=[
        "movie_name",
    ],
    how="outer",
    suffixes=("_a", "_b"),
)

cols_to_compare = ["country", "genres", "month", "year"]
for col in cols_to_compare:
    merged_df[col] = merged_df.apply(
        lambda row: (
            row[f"{col}_a"] if not pd.isna(row[f"{col}_a"]) else row[f"{col}_b"]
        ),
        axis=1,
    )

columns_to_drop = [col for col in merged_df.columns if col.endswith(("_a", "_b"))]
merged_df = merged_df.drop(columns=columns_to_drop, axis=1)

merged_df.dropna(subset=["country", "genres","ratings","user_vote"], inplace=True)
print(merged_df.info())
merged_df.to_csv("imdb_merged.csv", index=False)

'''

# Gộp dữ liệu từ critic_data.csv và imdb_merged.csv
'''
df_a = pd.read_csv("imdb_merged.csv")
df_b = pd.read_csv("critic_data.csv")
print(df_b.info())
df_b = df_b.dropna(subset=["critic_vote_rotten","critic_vote_metacritic","meta_score_metacritic","meta_score_rotten"],how = "all")
print(df_b.info())
merged_df = pd.merge(
    df_a,
    df_b,
    on=[
        "movie_name",
    ],
    how="outer",
    suffixes=("_a", "_b"),
)
print(merged_df.info())
merged_df["month"] = merged_df["month_a"]
merged_df["year"] = merged_df["year_a"]
columns_to_drop = [col for col in merged_df.columns if col.endswith(("_a", "_b"))]
merged_df = merged_df.drop(columns=columns_to_drop, axis=1)
merged_df.drop(columns = ["critic_vote_rotten","critic_vote_metacritic","meta_score_metacritic","meta_score_rotten"], axis=1, inplace=True)
merged_df = merged_df.dropna(subset = ["critic_vote","meta_score"], how = "all")
print(merged_df.info())
merged_df.to_csv("critic_merged.csv", index=False)
'''

# Gộp dữ liệu từ critic_merged.csv và themoviedb.csv

df_a = pd.read_csv("critic_merged.csv")
df_b = pd.read_csv("../themoviedb/data/all_data_themoviedb.csv")
merged_df = pd.merge(
    df_a,
    df_b,
    on=[
        "movie_name",
    ],
    how="outer",
    suffixes=("_a", "_b"),
)
print(merged_df.info())
merged_df["month"] = merged_df["month_a"]
merged_df["year"] = merged_df["year_a"]
columns_to_drop = [col for col in merged_df.columns if col.endswith(("_a", "_b"))]
merged_df = merged_df.drop(columns=columns_to_drop, axis=1)

print(merged_df.info())



# Hàm sửa đổi cột "genres"
def fix_genres(genres_str):
    genres = genres_str.split()
    if "Music" in genres and "Musical" in genres:
        genres.remove("Music")
    else:
        genres = [genre.replace("Music", "Musical") for genre in genres]
        genres = [genre.replace("Musicalal", "Musical") for genre in genres]
    return " ".join(genres)


# Áp dụng hàm sửa đổi cho cột "genres"
merged_df["genres"] = merged_df["genres"].apply(fix_genres)

merged_df.drop(["tt_id","rl_id"],axis=1,inplace = True)
merged_df.to_csv("final_merged.csv", index=False)
