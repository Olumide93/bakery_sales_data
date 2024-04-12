import streamlit as st
import numpy as np
import pandas as pd #You can't use pandas without numpy
import matplotlib.pyplot as plt


#load data
@st.cache_data
def load_data():
    df = pd.read_csv('bakerysales.csv')

    #data cleaning steps 
    df.drop(columns='Unnamed: 0', inplace=True)
    # dropping the unnamed column
    df['date'] = pd.to_datetime(df.date)
    # converting the date format from float to date
    # df['ticket_number'] = df.ticket_number.astype('object')
    # converting the ticket number from float to object
    df['unit_price'] = df.unit_price.str.replace(',','.').str.replace('€','')
    # converting to string and replacing comma and €
    df['unit_price'] = df.unit_price.astype('float')
    #converting the type from string  to float
    df.rename(columns={'unit_price': 'unit_price (€)',
                  'Quantity':'quantity'}, inplace=True)
    # renaming columns

    # calculate sales
    sales = df.quantity * df['unit_price (€)']
    # add a new column to the dataframe
    df['sales'] = sales
    # return cleaned dataframe
    return df

df = load_data()
st.title('Bakery Sales App')
# it adds a title to the web application. App structure

st.sidebar.title('Filters')
# it adds a sidebar to the left of the application. It is collapsibe and expandable. App structure

st.subheader('Data Preview')
st.dataframe(df.head())
# display the dataset

# create a filter for articles and ticket numbers
articles = df['article'].unique()
ticket_numbers = df['ticket_number'].value_counts().head(10).reset_index()['ticket_number']

# create a multiselect for articles. The variable selected_articles is stored as a list.
selected_articles = st.sidebar.multiselect('Products',articles)
top10_ticketNos = st.sidebar.selectbox('Top 10 Tickets',ticket_numbers[:10])

# filter
filtered_articles = df[df['article'].isin(selected_articles)]

# display the filtered table
st.subheader('Filtered table')
if not selected_articles:
    st.error('select an article')
else:
    st.dataframe(filtered_articles.sample(3))
# to use the sample function, you have to select an option

#Calculations
total_sales = int(df['sales'].sum())
total_quantity = int(df['quantity'].sum())
no_articles = len(articles)
# no_articles2 = df['article'].nunique()
no_filtered_articles = filtered_articles['article'].nunique()
total_filtered_sales = np.round(filtered_articles['sales'].sum(),2)
total_filtered_quantity = np.round(filtered_articles['quantity'].sum(),2)
#  display in columns
col1, col2, col3, col4 = st.columns(4)

if not selected_articles:
    col1.metric('Total Sales',f'{total_sales:,}')
else:
    col1.metric('Total Sales',total_filtered_sales)

if not selected_articles:
    col2.metric('Total Quantity Sold', f'{total_quantity:,}')
else:
    col2.metric('Total Quantity Sold', total_filtered_quantity)
# col4.metric('Number of Articles',no_articles)

# to show number of articles based on filter
if not selected_articles:
    col3.metric('No. of Products', no_articles)
else:
    col3.metric('No. of Products', no_filtered_articles)


# charts
st.header('Plotting')
# data
article_grp = df.groupby('article')['sales'].sum()
article_grp = article_grp.sort_values(ascending=False)[:-3]
table = article_grp.reset_index()

# selection from the filter
filtered_table = table[table['article'].isin(selected_articles)]

# bar plot
st.subheader('Bar Chart')
fig1, ax1 = plt.subplots(figsize=(10,6))
ax1.bar(filtered_table['article'],filtered_table['sales'])
st.pyplot(fig1)

# pie chart
# percentages
st.subheader('Pie Chart')
fig2, ax2 = plt.subplots(figsize=(7,5))
ax2.pie(filtered_table['sales'],
        labels = selected_articles,
        autopct = '%1.1f%%')
st.pyplot(fig2)

# trend analysis
st.subheader('Trend Analysis')
daily_sales = df.groupby('date')['sales'].sum()

fig3, ax3 =plt.subplots(figsize = (12,6))
ax3.plot(daily_sales.index, daily_sales.values)
st.pyplot(fig3)