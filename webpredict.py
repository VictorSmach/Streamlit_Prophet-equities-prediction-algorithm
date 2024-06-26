!pip install streamlit
import streamlit as st
from datetime import date

import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
Today = date.today().strftime("%Y-%m-%d")

st.title("Stock Prediction App")

stocks = ("EURAUD","NIO","AAPL", "GOOG", "MSFT", "GME", "EXAS") 

selected_stock = st.selectbox("select dataset for prediction", stocks) 
n_years =  st.slider("Years of prediction:", 1, 4)
period = n_years* 365

@st.cache
def load_data(ticker):
    data = yf.download(ticker,START,Today)
    data.reset_index(inplace = True)
    return data
    
data_load_state = st.text("Load data....")
data = load_data(selected_stock) 
data_load_state.text("Loading data....done")

st.subheader('Raw Data')
st.write(data.tail())

def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'] , y=data['Open'], name='Stock_Open'))
    fig.add_trace(go.Scatter(x=data['Date'] , y=data['Close'], name='Stock_Close'))
    fig.layout.update(title_text="Time series Data", xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

#Forecasting
df_train = data[['Date', 'Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet(daily_seasonality = True)
m.fit(df_train)
future = m.make_future_dataframe(periods = period)
forecast = m.predict(future)

st.subheader('Forecast Data')
st.write(forecast.tail())

st.write('Forecast Data')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write('forecast components')
fig2 = m.plot_components(forecast)
st.write(fig2)
