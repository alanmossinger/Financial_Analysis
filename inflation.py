import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# export the cpi data as a pd.DataFrame
def get_cpi_data(start_year=1913, end_year=2024):
    df = pd.read_excel("cpi_inflation_data.xlsx")
    df = df[(df["Year"] >= start_year) & (df["Year"] <= end_year)]
    return df


# visualize df
def visualize_cpi_data(df):
    df.plot(x="Year", y="Jan", title="CPI vs Year", legend=False)
    plt.show()

if __name__ == '__main__':
    df = get_cpi_data(start_year=1980)
    visualize_cpi_data(df)