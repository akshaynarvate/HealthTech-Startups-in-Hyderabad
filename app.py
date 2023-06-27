
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import openpyxl

# Read the data from the Excel file
data = pd.read_excel("HealthTech Hyd.xlsx")

# Set the page title
st.title('HealthTech Startups in Hyderabad')

# Display the first few rows of the dataset
st.subheader('Dataset')
st.dataframe(data.head())

# Display information about the dataset
st.subheader('Dataset Information')
st.write("Dataset Shape:", data.shape)
st.write("Number of Rows in the Dataframe:", data.shape[0])
st.write("Number of Columns in the Dataframe:", data.shape[1])


# Number of HealthTech Startups Founded Each Year
st.subheader('Number of HealthTech Startups Founded Each Year')

# Counting the number of startups founded each year
startup_count = data["Founding year"].value_counts().sort_index()

# Creating a bar trace
bar_trace = go.Bar(
    x=startup_count.index,
    y=startup_count.values,
    marker=dict(color='teal')
)

# Creating the layout
layout = go.Layout(
    title="Number of HealthTech Startups Founded Each Year",
    xaxis=dict(title="Year"),
    yaxis=dict(title="Count"),
    height=500,
    margin=dict(l=50, r=50, t=80, b=50)
)

# Creating the figure
fig = go.Figure(data=[bar_trace], layout=layout)

# Displaying the interactive chart
st.plotly_chart(fig)

## Funding Amount vs. Founding Year
st.subheader('Funding Amount vs. Founding Year')

# Clean and convert "Funding Received" column to numeric data type
data["Funding Received"] = data["Funding Received"].replace(r'[^\d.]', '', regex=True).astype(float)

# Create an interactive scatter plot using plotly's graph_objects
fig = go.Figure(data=go.Scatter(
    x=data['Founding year'],
    y=data['Funding Received'],
    mode='markers',
    marker=dict(
        size=10,
        color=data['Funding Received'],
        colorscale='Greens',
        showscale=True
    ),
    text=data['Startup name'],
    hovertemplate=(
        '<b>Startup:</b> %{text}<br>'
        '<b>Founding Year:</b> %{x}<br>'
        '<b>Funding Amount:</b> $%{y:,.2f}M<br>'
    )
))

fig.update_layout(
    title='Funding Amount vs. Founding Year',
    xaxis=dict(title='Founding Year'),
    yaxis=dict(
        title='Funding Amount',
        tickformat='$,-.2fM'
    ),
    hovermode='closest',
    height=600,
    showlegend=False,
    coloraxis=dict(
        colorbar=dict(
            title='Funding Amount',
            tickprefix='$',
            ticksuffix='M'
        )
    )
)

# Displaying the interactive chart
st.plotly_chart(fig)

## Top Investors in HealthTech space
st.subheader('Top Investors in HealthTech Space')

# Splitting the values in the Investors column
top_investors = data['Investors'].str.split(', ').explode().value_counts().nlargest(20)

# Reverse the order of the data
top_investors = top_investors.iloc[::-1]

# Create an interactive bar plot using plotly's graph_objects
fig = go.Figure(data=[go.Bar(x=top_investors.values, y=top_investors.index, orientation='h')])

fig.update_layout(
    title="Top Investors",
    xaxis=dict(title="Number of Startups"),
    yaxis=dict(title="Investor"),
    height=600,
    margin=dict(l=100, r=20, t=80, b=20),
)

# Displaying the interactive chart
st.plotly_chart(fig)



## Top Business Models in HealthTech startups
st.subheader('Top Business Models in HealthTech Startups')

# Splitting the values in the Business Model column
top_business_models = data['Business Model'].str.split(', ').explode().value_counts().nlargest(5)

# Reverse the order of the data
top_business_models = top_business_models.iloc[::-1]

# Create an interactive bar plot using plotly's graph_objects
fig = go.Figure(data=[go.Bar(x=top_business_models.values, y=top_business_models.index, orientation='h')])

fig.update_layout(
    title="Top Business Models",
    xaxis=dict(title="Number of Startups"),
    yaxis=dict(title="Business Models"),
    height=600,
    margin=dict(l=100, r=20, t=80, b=20),
)

# Displaying the interactive chart
st.plotly_chart(fig)


## Top Sectors of HealthTech startups
st.subheader('Top Sectors of HealthTech Startups')

# Splitting the values in the Focus sector column
top_sector = data['Focus sector'].str.split(', ').explode().value_counts().nlargest(20)

# Reverse the order of the data
top_sector = top_sector.iloc[::-1]

# Create an interactive bar plot using plotly's graph_objects
fig = go.Figure(data=[go.Bar(x=top_sector.values, y=top_sector.index, orientation='h')])

fig.update_layout(
    title="Top Sectors",
    xaxis=dict(title="Number of Startups"),
    yaxis=dict(title="Focus Sector"),
    height=600,
    margin=dict(l=100, r=20, t=80, b=20),
)

# Displaying the interactive chart
st.plotly_chart(fig)



## Distribution of Focus Sectors
st.subheader('Distribution of Focus Sectors')

# Splitting values in Focus sector column
sector_counts = data['Focus sector'].str.split(', ').explode().value_counts().nlargest(20)

# Creating an interactive pie chart using plotly's graph_objects
fig = go.Figure(data=[go.Pie(labels=sector_counts.index, values=sector_counts, hole=0.3)])

fig.update_layout(
    title="Distribution of Focus Sectors",
    annotations=[dict(text='Focus Sectors', x=0.5, y=0.5, font_size=20, showarrow=False)]
)

# Displaying the interactive chart
st.plotly_chart(fig)



## Distribution of Startup Enabler
st.subheader('Distribution of Startup Enabler')

# Value counting startup enabler
enabler = data["Enabler"].value_counts()

# Creating an interactive pie chart using plotly's graph_objects
fig = go.Figure(data=[go.Pie(labels=enabler.index, values=enabler, hole=0.3)])

fig.update_layout(title="Distribution of Startup Enabler")

# Displaying the interactive chart
st.plotly_chart(fig)



## Funding by Year and Sector
st.subheader('Funding by Year and Sector')

# Pivot table to aggregate funding by year and sector
pivot_table = data.pivot_table(
    index='Focus sector',
    columns='Founding year',
    values='Funding Received',
    aggfunc='sum'
)

# Display the heatmap using Seaborn
fig, ax = plt.subplots(figsize=(12, 18))
sns.heatmap(pivot_table, cmap='viridis', ax=ax)
plt.title('Funding by Year and Sector')
plt.xlabel('Founding Year')
plt.ylabel('Focus Sector')

# Display the heatmap in the Streamlit app
st.pyplot(fig)

