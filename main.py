import requests
import pandas as pd
#Retrieve Option Chain Data
def get_option_chain_data(instrument_name: str, expiry_date: str, access_token: str) -> pd.DataFrame:
    """
    Retrieve option chain data for both PE and CE options, returning highest bid for PE and highest ask for CE.
    
    Parameters:
    -----------
    instrument_name : str
        Instrument key from Upstox (e.g., "NSE_INDEX|Nifty 50")
    expiry_date : str
        Expiration date of the options in YYYY-MM-DD format
    access_token : str
        Authentication token for the Upstox API
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing option chain data with columns: instrument_name, strike_price, side, bid/ask
    """
    # API endpoint and headers
    url = 'https://api.upstox.com/v2/option/chain'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Query parameters
    params = {
        "mode": "option_chain",
        'instrument_key': instrument_name,
        'expiry_date': expiry_date
    }
    
    try:
        # Make API request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse response
        option_chain = response.json().get('data', [])

        if not option_chain:
            print(f"No option chain data found for {instrument_name} on {expiry_date}")
            return pd.DataFrame(columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
        
        # Process option chain data
        data_list = []
        for entry in option_chain:
            strike_price = entry['strike_price']

            # Process Put Options (PE) and retrieve highest bid price
            put_options = entry.get('put_options', {})
            put_bid_price = put_options.get('market_data', {}).get('bid_price')

            if put_bid_price is not None:
                data_list.append([
                    instrument_name, 
                    strike_price, 
                    'PE', 
                    put_bid_price  # Highest bid price for PE
                ])
                
            # Process Call Options (CE) and retrieve highest ask price
            call_options = entry.get('call_options', {})
            call_ask_price = call_options.get('market_data', {}).get('ask_price')

            if call_ask_price is not None:
                data_list.append([
                    instrument_name, 
                    strike_price, 
                    'CE', 
                    call_ask_price  # Highest ask price for CE
                ])
        
        # Create DataFrame from collected data
        df = pd.DataFrame(data_list, columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
        
        # Sort by strike price and side for consistency
        df = df.sort_values(['strike_price', 'side'])
        
        return df
    
    except requests.RequestException as e:
        print(f"API request error: {e}")
        return pd.DataFrame(columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame(columns=['instrument_name', 'strike_price', 'side', 'bid/ask'])
# Define the access token and parameters
access_token = 'your access_token'  # Replace with your actual access token
instrument_name = "NSE_INDEX|Nifty 50"
expiry_date = "2024-11-28"

# Fetch option chain data for both PE and CE
option_data = get_option_chain_data(instrument_name, expiry_date, access_token)

# Display the result
print(option_data)


#Calculate Margin and Premium Earned
def get_option_chain_data(instrument_name: str, expiry_date: str, access_token: str) -> pd.DataFrame:
    """
    Retrieve comprehensive option chain data for both PE and CE options.
    
    Parameters:
    -----------
    instrument_name : str
        Instrument key from Upstox (e.g., "NSE_INDEX|Nifty 50")
    expiry_date : str
        Expiration date of the options in YYYY-MM-DD format
    access_token : str
        Authentication token for the Upstox API
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing option chain data with specified columns.
    """
    # API endpoint and headers
    url = 'https://api.upstox.com/v2/option/chain'
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    # Query parameters
    params = {
        "mode": "option_chain",
        'instrument_key': instrument_name,
        'expiry_date': expiry_date
    }
    
    try:
        # Make API request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for bad responses

        # Parse response
        option_chain = response.json().get('data', [])

        if not option_chain:
            print(f"No option chain data found for {instrument_name} on {expiry_date}")
            return pd.DataFrame(columns=['instrument_key', 'instrument_name', 'strike_price', 'side', 'bid/ask', 'margin_required', 'premium_earned'])
        
        # Process option chain data
        data_list = []
        for entry in option_chain:
            strike_price = entry['strike_price']
            try:
                # Process Put Options (PE)
                put_options = entry.get('put_options', {})
                put_instrument_key = put_options.get('instrument_key')
                put_market_data = put_options.get('market_data', {})
                put_bid_price = put_market_data.get('bid_price')
                put_margin = put_market_data.get('margin_required', 0)

                if put_bid_price is not None and put_instrument_key is not None:
                    data_list.append([
                        put_instrument_key,
                        instrument_name, 
                        strike_price, 
                        'PE', 
                        put_bid_price,
                        put_margin,
                        put_bid_price * 100  # Example calculation for premium earned
                    ])
                
                # Process Call Options (CE)
                call_options = entry.get('call_options', {})
                call_instrument_key = call_options.get('instrument_key')
                call_market_data = call_options.get('market_data', {})
                call_ask_price = call_market_data.get('ask_price')
                call_margin = call_market_data.get('margin_required', 0)

                if call_ask_price is not None and call_instrument_key is not None:
                    data_list.append([
                        call_instrument_key,
                        instrument_name, 
                        strike_price, 
                        'CE', 
                        call_ask_price,
                        call_margin,
                        call_ask_price * 100 
                    ])
            except KeyError as e:
                print(f"Skipping entry due to missing key: {e}")
                continue
        
        # Create DataFrame from collected data
        df = pd.DataFrame(data_list, columns=['instrument_key', 'instrument_name', 'strike_price', 'side', 'bid/ask', 'margin_required', 'premium_earned'])
        
        # Sort by strike price and side for consistency
        df = df.sort_values(['strike_price', 'side'])
        
        return df
    
    except requests.RequestException as e:
        print(f"API request error: {e}")
        return pd.DataFrame(columns=['instrument_key', 'instrument_name', 'strike_price', 'side', 'bid/ask', 'margin_required', 'premium_earned'])
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame(columns=['instrument_key', 'instrument_name', 'strike_price', 'side', 'bid/ask', 'margin_required', 'premium_earned'])

def calculate_margin_and_premium(data: pd.DataFrame, access_token: str, lot_size: int = 100) -> pd.DataFrame:
    """
    Calculate margin required and premium earned for each option in the DataFrame.
    """

    # API endpoint and headers for margin calculation
    url = "https://api.upstox.com/v2/charges/margin"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Initialize lists to store calculated values
    margin_required_list = []
    premium_earned_list = []

    for index, row in data.iterrows():
        # Prepare data for margin calculation
        instrument_key = row['instrument_key']
        transaction_type = "SELL"
        quantity = lot_size

        payload = {
            "instruments": [
                {
                    "instrument_key": instrument_key,
                    "quantity": quantity,
                    "transaction_type": transaction_type,
                    "product": "D"
                }
            ]
        }
        try:
            # Make API request for margin calculation
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Raise an exception for bad responses
            # Extract margin required from the response
            response_data = response.json().get('data', {})  # Changed to dict access
            required_margin = response_data.get('required_margin', 0)  # Access required_margin
            margin_required_list.append(required_margin)
        except requests.RequestException as e:
            print(f"Error fetching margin for {instrument_key}: {e}")
            margin_required_list.append(None)
        # Calculate premium earned
        bid_ask_price = row['bid/ask']
        premium_earned = bid_ask_price * quantity if bid_ask_price is not None else 0
        premium_earned_list.append(premium_earned)
    # Add new columns to the DataFrame
    data['margin_required'] = margin_required_list
    data['premium_earned'] = premium_earned_list
    return data
# Example usage
if __name__ == "__main__":
    # Define the access token and parameters
    access_token = 'your_access_token'  # Replace with your actual token
    instrument_name = "NSE_INDEX|Nifty 50"
    expiry_date = "2024-11-28"
    
    # try:
    calculated_data = get_option_chain_data(instrument_name, expiry_date, access_token)

    if not calculated_data.empty:
        result_data = calculate_margin_and_premium(calculated_data, access_token)
        print("Option Chain Data with Margin and Premium:")
        print(result_data.to_string(index=False))
    else:
        print("No option data retrieved.")
    # except Exception as e:
    #     print(f"An error occurred: {e}")
