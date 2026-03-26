import pandas as pd
import numpy as np

class CarbonModel:
    def __init__(self, data):
        self.data = data
        self.scenario = {}

    def calculate_emissions(self):
        self.data['Total_Emissions'] = self.data['Production'] * self.data['Emission_Factor']
        self.data['Carbon_Intensity'] = self.data['Total_Emissions'] / self.data['Production']
        return self.data

    def apply_scenario(self, scenario):
        # Apply scenario to a copy of the data, not in-place
        scenario_data = self.data.copy()
        for key, value in scenario.items():
            if key in scenario_data.columns:
                scenario_data[key] = scenario_data[key] * value
        scenario_data['Total_Emissions'] = scenario_data['Production'] * scenario_data['Emission_Factor']
        scenario_data['Carbon_Intensity'] = scenario_data['Total_Emissions'] / scenario_data['Production']
        return scenario_data

    def forecast(self, years=5, growth_rate=0.05, scenario=None):
        forecasts = []
        emission_factor_multiplier = 1.0
        production_multiplier = 1.0
        if scenario:
            # Efficiency improvement increases production and reduces emission factor
            efficiency = scenario.get('Production', 1.0)
            energy_mix = scenario.get('Emission_Factor', 1.0)
            # For compounding, combine both effects for emission factor
            production_multiplier = efficiency
            # Emission factor is reduced by both energy mix and efficiency improvements
            emission_factor_multiplier = energy_mix / efficiency
        for i in range(years):
            forecast_data = self.data.copy()
            forecast_data['Year'] = forecast_data['Year'] + i + 1
            forecast_data['Production'] = forecast_data['Production'] * ((production_multiplier) ** (i + 1)) * ((1 + growth_rate) ** (i + 1))
            forecast_data['Emission_Factor'] = forecast_data['Emission_Factor'] * ((emission_factor_multiplier) ** (i + 1))
            forecast_data['Total_Emissions'] = forecast_data['Production'] * forecast_data['Emission_Factor']
            forecast_data['Carbon_Intensity'] = forecast_data['Total_Emissions'] / forecast_data['Production']
            forecasts.append(forecast_data)
        return pd.concat(forecasts, ignore_index=True)
