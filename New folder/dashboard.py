import streamlit as st
import pandas as pd
from models.carbon_model import CarbonModel

def load_data():
    return pd.read_csv('data/products.csv')

def main():
    st.title('Carbon Forecasting & Scenario Modeling Tool (FMCG)')
    data = load_data()
    model = CarbonModel(data)

    st.sidebar.header('Scenario Controls')
    energy_mix = st.sidebar.slider('Energy Mix Improvement (%)', 0, 100, 0)
    efficiency = st.sidebar.slider('Efficiency Improvement (%)', 0, 100, 0)
    growth = st.sidebar.slider('Production Growth Rate (%)', 0, 20, 5)
    years = st.sidebar.slider('Forecast Years', 1, 10, 5)

    scenario = {
        'Emission_Factor': 1 - energy_mix / 100,
        'Production': 1 + efficiency / 100
    }

    if st.sidebar.button('Apply Scenario'):
        scenario_data = model.apply_scenario(scenario)
        st.subheader('Scenario Results')
        st.dataframe(scenario_data)

    if st.sidebar.button('Forecast'):
        forecast_data = model.forecast(years=years, growth_rate=growth/100, scenario=scenario)
        st.subheader('Forecast Results')
        st.dataframe(forecast_data)

    st.subheader('Base Data')
    st.dataframe(data)

if __name__ == '__main__':
    main()
