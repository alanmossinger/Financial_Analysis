import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from inflation import get_cpi_data, visualize_cpi_data
import yfinance as yf

# ---------------------------------- DATA CLEANING ----------------------------------

inflation = get_cpi_data()
inflation.rename(columns={"Yea": "Year"}, inplace=True)
inflation.drop(columns=["HALF1", "HALF2"], inplace=True)
melted_inflation = inflation.melt(
        id_vars=["Year"],
        value_vars=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        value_name="CPI"
    )
# Mapping of month abbreviations to 0-indexed month indices
month_to_index = {
    "Jan": 0, "Feb": 1, "Mar": 2, "Apr": 3,
    "May": 4, "Jun": 5, "Jul": 6, "Aug": 7,
    "Sep": 8, "Oct": 9, "Nov": 10, "Dec": 11
}
# Replace the "Month" column with 0-indexed month indices
melted_inflation["variable"] = melted_inflation["variable"].map(month_to_index)
# sort the data by year and month
melted_inflation.sort_values(by=["Year", "variable"], inplace=True)



# open gold_annual.csv
# gold = pd.read_csv("assets/gold_monthly.csv")
# # expand date to date and month
# gold['Date'] = pd.to_datetime(gold['Date'])
# gold['Year'] = gold['Date'].dt.year
# # get month names
# gold['Month'] = gold['Date'].dt.month_name()
# # filter out data before 1913
# gold = gold[gold['Year'] >= 1913]

cmo = pd.read_excel("assets/cmo_all_commodities.xlsx", sheet_name="Monthly Prices")
# parse the date column, which has format YYYY"M"MM
cmo['Date'] = pd.to_datetime(cmo['Date'], format='%YM%m')
# expand date to year and month
cmo['Year'] = cmo['Date'].dt.year
cmo['Month'] = cmo['Date'].dt.month_name()


def get_inflation(start_year, month):
    """
    start_year: int - The year from which to start calculating inflation rates.
    month: str - The month for which to calculate inflation rates.

    Returns:
    np.series - A series containing the inflation rate for the given month starting from start_year.
    """
    CURR_YEAR = 2024
    CURR_MONTH = "December"

    # Get the inflation index for the current year and month
    curr_inflation = melted_inflation["CPI"].values[-1]

    # Filter the dataset for the given month starting from start_year to CURR_YEAR
    filtered_data = melted_inflation[(melted_inflation["Year"] >= start_year) & (melted_inflation["Year"] <= CURR_YEAR)]

    # Calculate inflation rates for the given month
    inflation_rates = filtered_data["CPI"] / curr_inflation

    return inflation_rates


def get_real_price(commodity_name, start_year=1960):
    """
    price: float
    year: int
    month: str
    """
    temp_df = cmo[cmo["Year"] >= start_year]
    commodity_prices = temp_df[commodity_name]
    # apply the get_inflation function to each row in gold
    inflation_series = get_inflation(start_year, "December")
    return commodity_prices.values / inflation_series.values

gld = get_real_price("Gold", start_year=1960)
silver = get_real_price("Silver", start_year=1960)
cu = get_real_price("Copper", start_year=1960)
platinum = get_real_price("Platinum", start_year=1960)

# normalize the prices
gld = gld / gld[0]
silver = silver / silver[0]
cu = cu / cu[0]
platinum = platinum / platinum[0]

# TODO fix the year, so that the np series accurately prints the years
# plot the real prices of gold, silver, copper, and platinum
plt.plot(gld, label="Gold")
plt.plot(silver, label="Silver")
plt.plot(cu, label="Copper")
plt.plot(platinum, label="Platinum")
plt.legend()
plt.title("Real Prices of Gold, Silver, Copper, and Platinum")
plt.xlabel("Year")
plt.ylabel("Price")
plt.show()
