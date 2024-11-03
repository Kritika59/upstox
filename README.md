# Options Trading Data Analysis

## Overview

This project is designed to interact with the Upstox API for retrieving options trading data, specifically for Call (CE) and Put (PE) options. It provides functionality to fetch option chain data and calculate trading metrics such as the required margin and premium earned from options trading.

## Table of Contents

- [Code Structure](#code-structure)
- [Functions](#functions)
- [get_option_chain_data](#get_option_chain_data)
- [calculate_margin_and_premium](#calculate_margin_and_premium)
- [Libraries Used](#libraries-used)
- [Specific Details About the Approach](#specific-details-about-the-approach)
- [Conclusion](#conclusion)

## Code Structure

The code consists of two main functions designed to fetch and analyze options data:

### Functions

#### `get_option_chain_data`

**Purpose**:  
Retrieve option chain data for specified instruments and expiry dates, capturing the highest bid for Put options (PE) and the highest ask for Call options (CE).

**Parameters**:
- `instrument_name`: A string representing the instrument key from Upstox (e.g., `"NSE_INDEX|Nifty 50"`).
- `expiry_date`: A string specifying the expiration date of the options in the format YYYY-MM-DD.
- `access_token`: A string for authenticating requests with the Upstox API.

**Returns**:  
A Pandas DataFrame containing columns: `instrument_name`, `strike_price`, `side` (indicating CE or PE), and `bid/ask`.

**Logic**:
1. Constructs a GET request to the Upstox API at the endpoint `https://api.upstox.com/v2/option/chain`, setting necessary headers for content type and authorization.
2. Sends the request and checks for errors.
3. Parses the response, extracting relevant option data (both CE and PE) and collects it into a list.
4. Creates a DataFrame from the collected data, sorted by `strike_price` and `side` for consistency.
5. Handles exceptions for network issues and unexpected API responses, returning an empty DataFrame in case of errors.

---

#### `calculate_margin_and_premium`

**Purpose**:  
Calculate the margin required for selling options and the premium earned for each option in the DataFrame obtained from `get_option_chain_data`.

**Parameters**:
- `data`: A Pandas DataFrame containing option chain data.
- `access_token`: A string for authenticating requests with the Upstox API.
- `lot_size`: An optional integer (defaulting to 100) representing the quantity of options to be traded.

**Returns**:  
The original DataFrame enriched with two new columns: `margin_required` and `premium_earned`.

**Logic**:
1. Iterates over each row of the DataFrame, preparing a POST request to the Upstox API at the endpoint `https://api.upstox.com/v2/charges/margin`.
2. Handles margin calculation responses, extracting the required margin and appending it to a list.
3. Calculates premium earned by multiplying the bid/ask price from the DataFrame by the lot size.
4. Adds the new columns for `margin_required` and `premium_earned` to the DataFrame.
5. Implements error handling to manage issues during API calls.

## Libraries Used

- **`requests`**: Used for making HTTP requests to the Upstox API, allowing data retrieval and submissions.
- **`pandas`**: A powerful library for data manipulation and analysis, used to manage the retrieved data efficiently.

## Specific Details About the Approach

- **Use of API**: The Upstox API provides real-time data necessary for options trading analysis, requiring valid access tokens for authentication.
- **Data Handling**: Utilization of Pandas DataFrames allows for easy manipulation of tabular data, facilitating calculations and integration of additional analyses.
- **Modular Design**: The modular code structure promotes clarity and maintainability, allowing for easy testing and future feature enhancements.
- **Error Handling**: Robust error handling enhances user experience by preventing abrupt crashes due to network issues or unexpected API responses.

## Conclusion

This code serves as a foundational tool for options trading analysis by leveraging the Upstox API to retrieve critical trading data and calculate important trading metrics. Its modular design, error handling, and reliance on robust libraries make it a valuable asset for traders looking to analyze options data programmatically. By understanding each function's purpose and logic, users can customize the script to fit their specific trading strategies and analysis needs.

