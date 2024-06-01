from flask import Flask, render_template, request, jsonify, send_from_directory
from predict_with_efa import *

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'app', 'templates'), filename)

# @app.route('/predict', methods=['GET'])
# def render_predict():
#     return render_template('predict.html')

# @app.route('/data', methods=['GET'])
# def render_data():
#     return render_template('table.html')

@app.route('/predict', methods=['POST'])
def process_prediction():
    data = request.json

    if data.get('openingWeek'):
        prediction_result_rf = predict_with_feature_selection("../model_efa/model_rf.pkl", data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['openingWeek'], data['userVote'], data['ratings'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_gb = predict_with_feature_selection("../model_efa/model_gb.pkl", data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['openingWeek'], data['userVote'], data['ratings'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_xgb = predict_with_feature_selection("../model_efa/model_xgb.pkl", data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['openingWeek'], data['userVote'], data['ratings'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_lgbm = predict_with_feature_selection("../model_efa/model_lgbm.pkl", data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['openingWeek'], data['userVote'], data['ratings'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_cb = predict_with_feature_selection("../model_efa/model_cb.pkl", data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['openingWeek'], data['userVote'], data['ratings'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
    else:
        prediction_result_rf = predict_with_feature_selection_without_opening_week("../model_efa/model_rf_without_opening_week.pkl" ,data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_gb = predict_with_feature_selection_without_opening_week("../model_efa/model_gb_without_opening_week.pkl" ,data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_xgb = predict_with_feature_selection_without_opening_week("../model_efa/model_xgb_without_opening_week.pkl" ,data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_lgbm = predict_with_feature_selection_without_opening_week("../model_efa/model_lgbm_without_opening_week.pkl" ,data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])
        prediction_result_cb = predict_with_feature_selection_without_opening_week("../model_efa/model_cb_without_opening_week.pkl" ,data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['criticVote'], data['metaScore'], data['sequel'], data['genres'], data['country'])

    print(prediction_result_rf)
    print(prediction_result_gb)
    print(prediction_result_xgb)
    print(prediction_result_lgbm)
    print(prediction_result_cb)
    
    return jsonify({'prediction_rf': float(prediction_result_rf), 'prediction_gb': float(prediction_result_gb), 'prediction_xgb': float(prediction_result_xgb), 'prediction_lgbm': float(prediction_result_lgbm), 'prediction_cb': float(prediction_result_cb)})

if __name__ == '__main__':
    app.run(debug=True)
