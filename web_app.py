import streamlit as st
from PIL import Image
import pandas as pd
from model import open_data, preprocess_data, split_data, load_model_and_predict

def process_main_page():
    show_main_page()
    process_sidebar_inputs()

def show_main_page():
    icon = Image.open("data/titanik_icon.png")

    st.set_page_config(
        layout="wide",
        initial_sidebar_state="auto",
        page_title="Cosmo Titanic",
        page_icon=icon
    )

    st.write("""
        # Классификация пассажиров космического коробля Титаник
        Предсказываем, кто перенесся в аномальию, а кто - нет.
        """)
    
    st.image("data/cosmo_titanik.png")


def write_user_data(df):
    st.write("### Ваши данные:")
    st.write(df)

def write_prediction(prediction, prediciton_probas):
    st.write("### Предсказания:")
    st.write(prediction)

    st.write("### Вероятность предсказания:")
    st.write(prediciton_probas)

def process_sidebar_inputs():
    st.sidebar.header("Параметры пассажира")
    user_inputs_df = sidebar_inputs_features()

    train_df = open_data()
    train_X_df, _ = split_data(train_df)
    full_X_df = pd.concat((user_inputs_df, train_X_df), axis=0)
    preprocessed_X_df = preprocess_data(full_X_df, test=False)


    user_X_df = preprocessed_X_df[:1]
    write_user_data(user_X_df)

    prediction, prediction_proba = load_model_and_predict(user_X_df)
    write_prediction(prediction, prediction_proba)
    
def sidebar_inputs_features():
    home_planet = st.sidebar.selectbox("Домашняя планета", ("Земля", "Европа", "Марс"))
    cryo_sleep = st.sidebar.selectbox("Криогенный сон", ("Да", "Нет"))
    destination = st.sidebar.selectbox("Место назначения", ("TRAPPIST-1e", "55 Cancri e", "PSO J318.5-22"))
    vip = st.sidebar.selectbox("VIP обслуживание", ("Да", "Нет"))

    age = st.sidebar.slider("Возвраст", min_value=1, max_value=80, value=20, step=1)


    translation = {
        "Земля": "Earth",
        "Европа": "Europa",
        "Марс": "Mars",
        "Да": True,
        "Нет": False,
        "TRAPPIST-1e": "TRAPPIST-1e",
        "55 Cancri e": "55 Cancri e",
        "PSO J318.5-22": "PSO J318.5-22",
    }

    data = {
        "HomePlanet": translation[home_planet],
        "CryoSleep": translation[cryo_sleep],
        "Destination": translation[destination],
        "Age": age,
        "VIP": translation[vip]
    }

    df = pd.DataFrame(data, index=[0])

    return df


if __name__ == "__main__":
    process_main_page()