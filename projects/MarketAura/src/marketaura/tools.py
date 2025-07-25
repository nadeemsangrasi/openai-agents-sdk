from agents import function_tool
import requests

@function_tool
def get_coins_id_by_names(coin_names: list[str]):
    """
    Retrieves the ID for a list of cryptocurrency names from Coinlore API.
    Searches across 'name', 'nameid', and 'symbol' fields, handling pagination.

    Args:
        coin_names: A list of cryptocurrency names or symbols (e.g., ["Bitcoin", "bitcoin", "BTC", "Ethereum", "eth"]).

    Returns:
        A list of dictionaries, where each dictionary contains 'name' and 'id'
        for the found coins.
    """
    found_coins_with_ids = []
    
    # Normalize input names to lowercase and use a set for efficient lookup
    remaining_input_names_lower = {name.lower() for name in coin_names}
    
    start_offset = 0
    limit = 100 
    total_api_coins = float('inf') # Sentinel value to ensure first API call

    # Continue fetching as long as there are names to find AND more coins available from API
    while remaining_input_names_lower and start_offset < total_api_coins: 
        url = f"https://api.coinlore.net/api/tickers/?start={start_offset}&limit={limit}"
        
        try:
            response = requests.get(url)
            response.raise_for_status() 
            data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break 
        
        coins_data = data.get('data')
        if not coins_data: # No more data in response
            break

        # On the first successful fetch, update the total count of coins from the API
        if total_api_coins == float('inf'):
             total_api_coins = data.get('info', {}).get('coins_num', 0)

        # Iterate through the coins in the current API response batch
        # We can directly modify remaining_input_names_lower because we're not iterating over it directly
        # and we use a copy for the check
        
        # Collect matches in this batch and remove them from the set of remaining names
        # Create a copy for safe iteration while modifying the original set
        for input_name_lower in list(remaining_input_names_lower): 
            for coin in coins_data:
                # Prepare coin data for case-insensitive comparison
                coin_identifiers = {
                    coin.get('name', '').lower(),
                    coin.get('nameid', '').lower(),
                    coin.get('symbol', '').lower()
                }
                
                if input_name_lower in coin_identifiers:
                    found_coins_with_ids.append({'name': coin['name'], 'id': coin['id']})
                    remaining_input_names_lower.remove(input_name_lower)
                    break # Break inner loop: this input_name_lower is found, move to next input
            
        start_offset += limit # Prepare for next page fetch
    
    # Optional: print the final offset to see how many API calls were made (for debugging/info)
    # print("Final offset:", start_offset)
    return found_coins_with_ids

import requests

@function_tool
def getAllCoinsTool():
    """
    Fetches a list of all available cryptocurrencies and their ticker information
    from the CoinLore API.

    Returns:
        list: A list of dictionaries, where each dictionary represents a cryptocurrency
              and its ticker data. Returns an empty list if an error occurs.
    """
    url = 'https://api.coinlore.net/api/tickers/'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching all coins: {e}")
        return []

@function_tool
def getCoinsByIDs(coins_ids: list[str]):
    """
    Fetches ticker information for a list of specified cryptocurrencies by their IDs.

    Args:
        coins_ids (list[str]): A list of string IDs for the cryptocurrencies to retrieve.

    Returns:
        list: A list of dictionaries, where each dictionary represents a cryptocurrency
              and its ticker data. Returns an empty list if an error occurs.
    """
    params = ",".join(coins_ids)
    url = f'https://api.coinlore.net/api/ticker/?id={params}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching coins by IDs: {e}")
        return []

@function_tool
def socialStatsTool(coin_id: str):
    """
    Fetches social statistics for a specific cryptocurrency by its ID.

    Args:
        coin_id (str): The ID of the cryptocurrency.

    Returns:
        dict: A dictionary containing social statistics for the specified coin.
              Returns an empty dictionary if an error occurs or data is not found.
    """
    url = f'https://api.coinlore.net/api/coin/social_stats/?id={coin_id}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching social stats for coin ID {coin_id}: {e}")
        return {} # Changed to return empty dict as social stats is typically a single object

@function_tool
def getAllExchanges():
    """
    Fetches a list of all cryptocurrency exchanges from the CoinLore API.

    Returns:
        list: A list of dictionaries, where each dictionary represents a cryptocurrency exchange.
              Returns an empty list if an error occurs.
    """
    url = f'https://coinlore.net/api/exchanges/' # Corrected URL path based on common CoinLore patterns

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching all exchanges: {e}")
        return []

@function_tool
def getExchangesByIds(exchange_id: str):
    """
    Fetches detailed information for a specific cryptocurrency exchange by its ID.

    Args:
        exchange_id (str): The ID of the cryptocurrency exchange.

    Returns:
        dict: A dictionary containing detailed information for the specified exchange.
              Returns an empty dictionary if an error occurs or data is not found.
    """
    url = f'https://api.coinlore.net/api/exchange/?id={exchange_id}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching exchange by ID {exchange_id}: {e}")
        return {} # Changed to return empty dict as exchange data is typically a single object

@function_tool
def marketDataForCoins(coin_id: str):
    """
    Fetches market data (e.g., trading pairs, volumes) for a specific cryptocurrency by its ID.

    Args:
        coin_id (str): The ID of the cryptocurrency.

    Returns:
        list: A list of dictionaries, where each dictionary represents market data
              for the specified coin. Returns an empty list if an error occurs.
    """
    url = f'https://api.coinlore.net/api/coin/markets/?id={coin_id}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching market data for coin ID {coin_id}: {e}")
        return []