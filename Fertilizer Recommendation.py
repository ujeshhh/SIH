import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error
import tkinter as tk
from tkinter import messagebox

soil_health_mapping = {
    "Poor": 2,
    "Average": 5,
    "Good": 7,
    "Excellent": 10
}

weather_pattern_mapping = {
    "Sunny": 10,
    "Rainy": 5,
    "Cloudy": 7,
    "Windy": 3
}

def Model(file_path):
    data = pd.read_csv('D:\SIH Hackathon\Py Files\DataM.csv')

    le_crop_type, le_fertilizer_type = LabelEncoder(), LabelEncoder()
    data['crop_type_encoded'] = le_crop_type.fit_transform(data['crop_type'])
    data['fertilizer_type_encoded'] = le_fertilizer_type.fit_transform(data['fertilizer_type'])

    X = data[['soil_health', 'weather_pattern', 'crop_type_encoded']]
    y_fertilizer_type = data['fertilizer_type_encoded']
    y_fertilizer_amount = data['fertilizer_amount']

    X_train_type, X_test_type, y_train_type, y_test_type = train_test_split(X, y_fertilizer_type, test_size=0.2, random_state=42)
    X_train_amount, X_test_amount, y_train_amount, y_test_amount = train_test_split(X, y_fertilizer_amount, test_size=0.2, random_state=42)

    rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42).fit(X_train_type, y_train_type)
    rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train_amount, y_train_amount)

    y_pred_type = rf_classifier.predict(X_test_type)
    accuracy = accuracy_score(y_test_type, y_pred_type)

    y_pred_amount = rf_regressor.predict(X_test_amount)
    mse = mean_squared_error(y_test_amount, y_pred_amount)

    return rf_classifier, rf_regressor, le_crop_type, le_fertilizer_type, data, accuracy, mse

def predict_fertilizer():
    try:
        soil_health_input = soil_health_mapping[entry_soil_health.get()]
        weather_pattern_input = weather_pattern_mapping[entry_weather_pattern.get()]
        crop_type_input = entry_crop_type.get()

        crop_type_encoded = le_crop_type.transform([crop_type_input])[0]

        user_input = pd.DataFrame([[soil_health_input, weather_pattern_input, crop_type_encoded]],
                                  columns=['soil_health', 'weather_pattern', 'crop_type_encoded'])

        fertilizer_type_encoded = rf_classifier.predict(user_input)[0]
        fertilizer_amount = rf_regressor.predict(user_input)[0]

        fertilizer_type = le_fertilizer_type.inverse_transform([fertilizer_type_encoded])[0]
        low_cost_brand = data[data['fertilizer_type'] == fertilizer_type]['low_cost_brand'].values[0]

        messagebox.showinfo("Prediction Results",
                            f"Recommended fertilizer: {fertilizer_type}\n"
                            f"Amount: {fertilizer_amount:.2f}\n"
                            f"Low cost brand: {low_cost_brand}")

    except Exception:
        messagebox.showerror("Input Error", "Invalid input. Check values and try again.")

def init_ui(accuracy, mse):
    global entry_soil_health, entry_weather_pattern, entry_crop_type

    window = tk.Tk()
    window.title("Fertilizer Recommendation")
    window.geometry("1920x1080")

    legend_text = ("Input:\n"
                   "1. Soil Health: Choose one - [Poor,Average,Good,Excellent].\n"
                   "2. Weather Pattern: Choose one - [Sunny,Rainy,Cloudy,Windy].\n"
                   "3. Crop Type: Choose one - [Wheat,Corn,Rice,Maize,Cotton,Soybean]")
    tk.Label(window, text=legend_text, font=("Arial", 12), justify="left").pack(pady=10)

    tk.Label(window, text="Soil Health:", font=("Arial", 14)).pack(pady=10)
    entry_soil_health = tk.Entry(window, font=("Arial", 14), width=30)
    entry_soil_health.pack()

    tk.Label(window, text="Weather Pattern:", font=("Arial", 14)).pack(pady=10)
    entry_weather_pattern = tk.Entry(window, font=("Arial", 14), width=30)
    entry_weather_pattern.pack()

    tk.Label(window, text="Crop Type:", font=("Arial", 14)).pack(pady=10)
    entry_crop_type = tk.Entry(window, font=("Arial", 14), width=30)
    entry_crop_type.pack()

    tk.Button(window, text="GET RESULT", font=("Arial", 14), command=predict_fertilizer, width=20, height=2).pack(pady=30)

    window.mainloop()

file_path = 'D:\\SIH Hackathon\\Py Files\\DataM.csv'
rf_classifier, rf_regressor, le_crop_type, le_fertilizer_type, data, accuracy, mse = Model(file_path)
init_ui(accuracy, mse)

