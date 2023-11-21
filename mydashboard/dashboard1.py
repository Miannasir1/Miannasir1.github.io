import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')
import os

st.set_page_config(page_title="Sales Analysis", page_icon=":bar_chart:", layout="wide")

st.title(" :bar_chart: Sales Analysis \n Exploratory Data Analysis(EDA)")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Upload your dataset", type=["csv", "xlsx","xls","txt"])

if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename,encoding='ISO-8859-1')
    
else:
    os.chdir(r"/Users/apple/Desktop/AI Corvit/Module 2/streamproject")
    df = pd.read_csv("Sales_data.csv",encoding='ISO-8859-1')


# -----------------------------------------------


col1, col2 = st.columns((2))
df["Date"] = pd.to_datetime(df["Date"]) 

# getting the min and max date
startDate = pd.to_datetime(df["Date"]).min()
endDate = pd.to_datetime(df["Date"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))
df = df[(df["Date"] >= date1) & (df["Date"] <= date2)].copy()


#-------------------------------------------------



st.sidebar.header("choose your option")
city = st.sidebar.multiselect("Pick your City", df["City"].unique())


# create for City
if not city:
    df2 = df.copy()
else:
    df2 = df[df["City"].isin(city)]

# create for Customer type
customer = st.sidebar.multiselect("Pick Customer type", df2["Customer type"].unique())
if not customer:
    df3 = df2.copy()
else:
    df3 = df2[df2["Customer type"].isin(customer)]
# create for Product line
product = st.sidebar.multiselect("Pick your Product line", df3["Product line"].unique())
# filter the data based on region ,state and cities
# permition and combination


#-------------------------------------------------


if not city and not customer and not product:
    filtered_data = df
elif not customer and not product:
    filtered_data = df[df["City"].isin(city)]
elif not product and not city:
    filtered_data = df[df["Customer type"].isin(customer)]
elif customer and product:
    filtered_data = df3[df["Customer type"].isin(customer) & df3['Product line'].isin(product)]
elif city and product:
    filtered_data = df3[df["City"].isin(city) & df3['Product line'].isin(product)]
elif city and customer:
    filtered_data = df3[df["City"].isin(city) & df3['Customer type'].isin(customer)]
elif product:
    filtered_data = df3[df3['Product line'].isin(product)]
else:
    filtered_data = df3[df3['City'].isin(customer) & df3['Customer type'].isin(customer) & df3['Product line'].isin(product)]


#-------------------------------------------------


# column chart for category
category_df = filtered_data.groupby(by = ["Product line"], as_index=False)["Total"].sum()

with col1:
    st.subheader("Category wise Sales")
    fig=px.bar(category_df, x="Product line", y="Total", text = ['{:,.2f}'.format(x) for x in category_df["Total"]],
               template="seaborn")
    st.plotly_chart(fig, use_container_width=True,height=200)
with col2:
    st.subheader("City wise Sales %")
    fig=px.pie(filtered_data, values="Total", names="City", hole = 0.5)
    fig.update_traces(text = filtered_data["City"], textposition='outside')
    st.plotly_chart(fig, use_container_width=True,height=200)

cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap='Blues'))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("download Data", data=csv, file_name='category.csv', mime='text/csv',
                           help = 'Click here to download the data as a csv file')
with cl2:
    with st.expander("REGION_ViewData"):
        region = filtered_data.groupby(by = ["City"], as_index=False)["Total"].sum()
        st.write(region.style.background_gradient(cmap='Oranges'))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("download Data", data=csv, file_name='City.csv', mime='text/csv',
                           help = 'Click here to download the data as a csv file')

#-------------------------------------------------


filtered_data['month_year'] = filtered_data['Date'].dt.to_period('M')
st.subheader('Time series Analysis')
linechart = pd.DataFrame(filtered_data.groupby(filtered_data["month_year"].dt.strftime("%Y : %b"))["Total"].sum()).reset_index()
fig2 = px.line(linechart, x="month_year", y="Total",labels={"Total": "Amount"},height=500,width=1000,
               template="gridon")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of Time Series"):
    st.write(linechart.T.style.background_gradient(cmap='Blues'))
    csv = linechart.to_csv(index=False).encode('utf-8')
    st.download_button("download Data", data=csv, file_name='TimeSeries.csv', mime='text/csv',
                       help = 'Click here to download the data as a csv file')
    

#-------------------------------------------------


# create a tree map for sub category, region and category

st.subheader("Tree Map")
fig3 = px.treemap(filtered_data, path=["Product line",  "City"], values="Total", hover_data=["Total"])
fig3.update_layout(width=800,height=650)
st.plotly_chart(fig3, use_container_width=True) 

#-------------------------------------------------

chart1, chart2 = st.columns((2))
with chart1:
    st.subheader('Segment wise Sales')
    fig = px.pie(filtered_data, values = "Total", template = "plotly_dark")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader('Category wise Sales')
    fig = px.pie(filtered_data, values = "Total", names = "Product line", template = "gridon")
    fig.update_traces(text = filtered_data["Product line"], textposition = "inside")
    st.plotly_chart(fig,use_container_width=True)

import plotly.figure_factory as ff
st.subheader(":point_right: Month wise Sub-Category Sales Summary")
with st.expander("Summary_Table"):
    df_sample = df[0:5][["City","Customer type","Product line","Total","Tax 5%","Quantity"]]
    fig = ff.create_table(df_sample, colorscale = "Cividis")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    filtered_data["month"] = filtered_data["Date"].dt.month_name()
    sub_category_Year = pd.pivot_table(data = filtered_data, values = "Total",columns = "month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))

# Create a scatter plot
data1 = px.scatter(filtered_data, x = "Total", y = "Profit", size = "Quantity")
data1['layout'].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont = dict(size=20),xaxis = dict(title="Total",titlefont=dict(size=19)),
                       yaxis = dict(title = "Profit", titlefont = dict(size=19)))
st.plotly_chart(data1,use_container_width=True)

with st.expander("Data"):
    st.write(filtered_data.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Download orginal DataSet
csv = df.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")


