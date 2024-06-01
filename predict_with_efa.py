import pandas as pd
import numpy as np
import pickle
import os
import warnings
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# Dope,R,7000000.0,103.0,2002.0,6100010.0,17506470.0,7.2,89000.0,United States,Adventure Comedy Crime Drama,200.0,85.04,0,6.0,2015.0
# Dora and the Lost City of Gold,PG,49000000.0,102.0,3735.0,17431588.0,60477943.0,6.1,35000.0,"Australia, United States",Action Adventure Comedy Family Fantasy Mystery,179.0,82.17,0,8.0,2019.0
# Double Take,PG-13,24000000.0,88.0,1631.0,11736236.0,29831583.0,5.4,88000.0,United States,Action Comedy Crime Thriller,100.0,14.86,0,1.0,2001.0
# Doubt,PG-13,20000000.0,104.0,1287.0,507226.0,33446470.0,7.5,136000.0,United States,Drama Mystery,257.0,77.46,0,12.0,2008.0
# Down to Earth,PG-13,49000000.0,87.0,2521.0,20027309.0,64186502.0,5.4,25000.0,United States,Comedy Fantasy,124.0,22.71,0,2.0,2001.0
# Downsizing,R,68000000.0,135.0,2668.0,4954287.0,24449754.0,5.8,125000.0,United States,Drama Fantasy Sci-Fi,349.0,49.34,0,12.0,2017.0
# Downton Abbey,PG,13000000.0,122.0,3548.0,31033665.0,96853865.0,7.4,63000.0,United Kingdom,Drama Romance,303.0,81.23,0,9.0,2019.0
# Dr. Dolittle 2,PG,72000000.0,87.0,3053.0,25037039.0,112952899.0,4.7,47000.0,United States,Comedy Family Fantasy,135.0,42.66,0,6.0,2001.0
# Dracula 2000,R,54000000.0,100.0,2204.0,8636567.0,33022767.0,4.9,37000.0,"Canada, United States",Action Fantasy Horror Thriller,14.0,26.0,0,12.0,2000.0
# Dracula Untold,PG-13,70000000.0,92.0,2900.0,23514615.0,56280355.0,6.2,208000.0,United States,Action Drama Fantasy Horror,168.0,27.68,0,10.0,2014.0
# Draft Day,PG-13,25000000.0,110.0,2781.0,9783603.0,28842237.0,6.8,67000.0,United States,Drama Sport,196.0,58.99,0,4.0,2014.0
# Drag Me to Hell,PG-13,30000000.0,99.0,2510.0,15825480.0,42100625.0,6.6,218000.0,United States,Horror,302.0,91.05,0,5.0,2009.0
# Dragon Wars: D-War,PG-13,32000000.0,107.0,2277.0,5376000.0,10977721.0,3.5,25000.0,"Republic of Korea, United States",Action Drama Fantasy Thriller,47.0,29.77,0,9.0,2007.0
# Dragonball Evolution,PG,30000000.0,85.0,2181.0,4756488.0,9362785.0,2.5,79000.0,United States,Action Adventure Fantasy Sci-Fi Thriller,10.0,45.0,0,4.0,2009.0
# Dragonfly,PG-13,60000000.0,104.0,2507.0,10216025.0,30323400.0,6.1,40000.0,"Germany, United States",Drama Fantasy Mystery Romance Thriller,158.0,10.76,0,2.0,2002.0

def predict_with_feature_selection(movie, model_file_name):
    with open(model_file_name, "rb") as f:
        model = pickle.load(f)
    with open("model_efa/mpaa_label_encoder.pkl", "rb") as f:
        mpaa_label_encoder = pickle.load(f)
    with open("model_efa/country_label_encoder.pkl", "rb") as f:
        country_label_encoder = pickle.load(f)
    with open("model_efa/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("model_efa/factor_analyzer.pkl", "rb") as f:
        fa = pickle.load(f)
    with open("model_efa/unique_genres.pkl", "rb") as f:
        unique_genres = pickle.load(f)
    with open("model_efa/selected_features.pkl", "rb") as f:
        selected_features = pickle.load(f)

    movie["mpaa"] = mpaa_label_encoder.transform([movie["mpaa"]])[0]
    movie["country"] = country_label_encoder.transform([movie["country"]])[0]

    new_movie_genres = np.array(
        [
            1 if genre in movie.get("genres", "").split() else 0
            for genre in unique_genres
        ]
    ).reshape(1, -1)
    new_movie_genres_scaled = scaler.transform(new_movie_genres)
    new_movie_factors = fa.transform(new_movie_genres_scaled)

    movie.update(
        {
            f"Factor{i+1}": new_movie_factors[0, i]
            for i in range(new_movie_factors.shape[1])
        }
    )

    movie_df = pd.DataFrame([movie])
    movie_df = movie_df[selected_features]
    prediction_log = model.predict(movie_df)
    prediction = np.expm1(prediction_log)  
    return prediction[0]

def predict_with_feature_selection_without_opening_week(movie, model_file_name):
    with open(model_file_name, "rb") as f:
        model = pickle.load(f)
    with open("model_efa/mpaa_label_encoder.pkl", "rb") as f:
        mpaa_label_encoder = pickle.load(f)
    with open("model_efa/country_label_encoder.pkl", "rb") as f:
        country_label_encoder = pickle.load(f)
    with open("model_efa/scaler.pkl", "rb") as f:
        scaler = pickle.load(f)
    with open("model_efa/factor_analyzer.pkl", "rb") as f:
        fa = pickle.load(f)
    with open("model_efa/unique_genres.pkl", "rb") as f:
        unique_genres = pickle.load(f)
    with open("model_efa/selected_features_without_opening_week.pkl", "rb") as f:
        selected_features = pickle.load(f)

    movie["mpaa"] = mpaa_label_encoder.transform([movie["mpaa"]])[0]
    movie["country"] = country_label_encoder.transform([movie["country"]])[0]

    new_movie_genres = np.array(
        [
            1 if genre in movie.get("genres", "").split() else 0
            for genre in unique_genres
        ]
    ).reshape(1, -1)
    new_movie_genres_scaled = scaler.transform(new_movie_genres)
    new_movie_factors = fa.transform(new_movie_genres_scaled)

    movie.update(
        {
            f"Factor{i+1}": new_movie_factors[0, i]
            for i in range(new_movie_factors.shape[1])
        }
    )

    movie_df = pd.DataFrame([movie])
    movie_df = movie_df[selected_features]
    prediction_log = model.predict(movie_df)
    prediction = np.expm1(prediction_log)  
    return prediction[0]

def ret_movie(movie_str):
    movie_arr = movie_str.split(',')

    movie = {}

    movie["month"] = float(movie_arr[14])
    movie["year"] = float(movie_arr[15])
    movie["mpaa"] = movie_arr[1]
    movie["budget"] = float(movie_arr[2])
    movie["runtime"] = float(movie_arr[3])
    movie["screens"] = float(movie_arr[4])
    movie["opening_week"] = float(movie_arr[5])
    movie["user_vote"] = float(movie_arr[8])
    movie["ratings"] = float(movie_arr[7])
    movie["critic_vote"] = float(movie_arr[11])
    movie["meta_score"] = float(movie_arr[12])
    movie["sequel"] = float(movie_arr[13])
    movie["genres"] = movie_arr[10]
    movie["country"] = movie_arr[9]

    return movie

def ret_movie_without_opening_week(movie_str):
    movie_arr = movie_str.split(',')

    movie = {}

    movie["month"] = float(movie_arr[14])
    movie["year"] = float(movie_arr[15])
    movie["mpaa"] = movie_arr[1]
    movie["budget"] = float(movie_arr[2])
    movie["runtime"] = float(movie_arr[3])
    movie["screens"] = float(movie_arr[4])
    movie["critic_vote"] = float(movie_arr[11])
    movie["meta_score"] = float(movie_arr[12])
    movie["sequel"] = float(movie_arr[13])
    movie["genres"] = movie_arr[10]
    movie["country"] = movie_arr[9]

    return movie

movie_str = "Dora and the Lost City of Gold,PG,49000000.0,102.0,3735.0,17431588.0,60477943.0,6.1,35000.0,Australia United States,Action Adventure Comedy Family Fantasy Mystery,179.0,82.17,0,8.0,2019.0"
movie = ret_movie(movie_str)
movie_without_opening_week = ret_movie_without_opening_week(movie_str)

list_file_name = ["model_efa/model_rf.pkl", "model_efa/model_gb.pkl", "model_efa/model_xgb.pkl", "model_efa/model_lgbm.pkl", "model_efa/model_cb.pkl"]
list_file_name_without_opening_week = ["model_efa/model_rf_without_opening_week.pkl", "model_efa/model_gb_without_opening_week.pkl", "model_efa/model_xgb_without_opening_week.pkl", "model_efa/model_lgbm_without_opening_week.pkl", "model_efa/model_cb_without_opening_week.pkl"]


for file_name in list_file_name:
    movie_cpy = movie.copy()
    predicted_revenue = predict_with_feature_selection(movie_cpy, file_name)    
    print("------------------------------------------------------------------")
    print(file_name)
    print("Predicted revenue:", predicted_revenue)
    print("Chênh lệch: ", str(predicted_revenue - float(movie_str.split(",")[6])))

for file_name in list_file_name_without_opening_week:
    movie_cpy = movie_without_opening_week.copy()
    predicted_revenue = predict_with_feature_selection_without_opening_week(movie_cpy, file_name)    
    print("------------------------------------------------------------------")
    print(file_name)
    print("Predicted revenue:", predicted_revenue)
    print("Chênh lệch: ", str(predicted_revenue - float(movie_str.split(",")[6])))