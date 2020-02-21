import os
from urllib.request import urlretrieve

import pandas as pd

EXCEL = os.path.join(".", "order_data.xlsx")
if not os.path.isfile(EXCEL):
    urlretrieve("https://bites-data.s3.us-east-2.amazonaws.com/order_data.xlsx", EXCEL)


def load_excel_into_dataframe(excel=EXCEL):
    """Load the SalesOrders sheet of the excel book (EXCEL variable)
       into a Pandas DataFrame and return it to the caller"""
    df = pd.read_excel(excel, sheet_name="SalesOrders")
    return df


def get_year_region_breakdown(df):
    """Group the DataFrame by year and region, summing the Total
       column. You probably need to make an extra column for
       year, return the new df as shown in the Bite description"""
    df = df.copy()
    df["Year"] = df["OrderDate"].dt.year
    df = df.groupby(by=["Year", "Region"])["Total"].sum()
    return df


def get_best_sales_rep(df):
    """Return a tuple of the name of the sales rep and
       the total of his/her sales"""
    df = df.groupby("Rep")["Total"].sum()
    return df.idxmax(), df.max()


def get_most_sold_item(df):
    """Return a tuple of the name of the most sold item
       and the number of units sold"""
    df = df.groupby("Item")["Units"].sum()
    return df.idxmax(), df.max()
