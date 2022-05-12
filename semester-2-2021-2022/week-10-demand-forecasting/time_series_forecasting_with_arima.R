library(ggplot2)
library(ggfortify)
library(tsdl)
library(tseries)
library(forecast)

gas <- window(UKgas, start=1960, end=1982.9)
gas
test <- window(UKgas, start=1983)
test

autoplot(gas) + ggtitle('Gas consumpition in the UK')
autoplot(decompose(gas, type='multiplicative'))
autoplot(ma(gas, 4), series='4-MA') + ggtitle('Moving average of gas consumpition in the UK')

# Make time series stationary
gas_stationary <- diff(gas)
gas_stationary <- diff(gas_stationary, 4)
autoplot(gas_stationary)

# Augmented Dickey–Fuller Test for stationarity
# low p-value => stationary
options(warn=-1)
adf.test(gas_stationary)     

# Kwiatkowski-Phillips-Schmidt-Shin (KPSS) for level or trend stationarity
kpss.test(gas_stationary, null="Trend")

# ACF - Moving Average order
ggAcf(gas)
# PACF - Auto regression order
ggPacf(gas)

arima_gas <- arima(gas, order=c(3,1,1), seasonal=c(1,1,1))
arima_gas

ggtsdiag(arima_gas)

# P-value should be bigger than 0.05 
# signifies independence of residuals
checkresiduals(arima_gas, lag=36)

forecast_gas <- forecast(arima_gas, level=c(95), h=c(16))
forecast_gas
autoplot(forecast_gas)

accuracy(forecast(arima_gas, h=16), UKgas)

# Call ARIMAs exhausting hyperparameter search to validate
auto.arima(gas, stepwise = FALSE, approximation = FALSE)
