# Problem B: Analysis of Demand for Express Services

## Background

This study focuses on the analysis of express delivery demand in the context of the development of China’s modern logistics industry. The objectives include quantifying the importance of cities within the logistics network, forecasting future delivery trends and volumes, predicting sudden disruptions in delivery routes, optimizing the inter-city transportation network, and mathematically defining fixed and non-fixed demand constants. These analyses hold significant practical value for professionals in the logistics sector.

## Data Preprocessing

The express delivery data provided in the problem is time series data with evident missing values. Based on the problem description, we performed reasonable imputation for the missing values, thereby improving the stationarity of the series and laying the foundation for subsequent ARIMA-based forecasting.

## Problem 1

For Problem 1, four indicators were selected to quantify a city’s importance: the number of packages received, the number of packages sent, the number of upstream cities, and the number of downstream cities. To reasonably assign weights to these indicators, we adopted the **PageRank algorithm** proposed by Google, which comprehensively considers the connectivity of cities within the logistics network and their activity in terms of express delivery. The final results show that the top five cities in terms of importance are: L, G, V, X, and R.

## Problem 2

For Problem 2, the data is strictly time-series in nature. After differencing and other stationarity processing techniques, we employed the **ARIMA time series model** to forecast express delivery volumes between cities on the specified dates, thereby obtaining the distribution of package flows between origin-destination city pairs.

## Problem 3

For Problem 3, observations reveal that for most delivery routes, express volumes significantly decline in the week prior to entering a suspended state and sharply rebound once normal service resumes. Based on this, we applied a decision tree algorithm to classify each route’s time series using a 7-day sliding window, predicting whether the route would be operational in the near future. Additionally, considering that such disruptions may exhibit periodic characteristics, we continued using the **ARIMA model** from Problem 2 to predict delivery volumes during the specified time period.

## Problem 4

For Problem 4, considering practical constraints, we used both **heuristic algorithms** and **mixed-integer linear programming (MILP)** models to optimize the delivery network from April 23 to April 27, 2023. The heuristic algorithm combines greedy strategies and local search to quickly find near-optimal solutions, while the MILP model ensures global optimality through exact solving. Both approaches take into account constraints such as not exceeding the rated loading capacity and minimizing the number of paths between city pairs. The resulting minimum transportation costs for the five days are: 948.34, 1009.35, 972.85, 923.02, 897.60, respectively.

## Problem 5

For Problem 5, we used the **STL decomposition method** to break down the time series into trend, seasonal, and residual components. The average of the quarterly trend components is defined as the fixed demand constant, while the mean and standard deviation of the seasonal component are used as parameters for the probability distribution of non-fixed demand. Furthermore, the accuracy of this seasonal decomposition approach was validated using the **XGBoost backtesting method**, which achieved a prediction accuracy of 0.87, demonstrating the effectiveness of the model.
