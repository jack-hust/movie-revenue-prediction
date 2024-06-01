from feature_selection import *

df_old = pd.read_csv("merge_data/final_merged.csv")
df_new = pd.read_csv("merge_data/movies_data.csv")

df = pd.concat([df_old, df_new], ignore_index=True)
df.drop_duplicates(inplace=True)

df.to_csv("merge_data/final_merged.csv", index=False)

train(df)
train_without_opening_week(df)