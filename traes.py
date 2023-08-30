import MetaTrader5 as mt5

# Constants for connection settings
SERVER = "BrokerServer"
LOGIN = "YourLogin"
PASSWORD = "YourPassword"

# Constants for XAUUSD symbol
SYMBOL = "XAUUSD"
TIMEFRAME = mt5.TIMEFRAME_M5

# Function to check for a double top pattern
def is_double_top(rates):
    if len(rates) < 5:
        return False

    highest_high = max(rates[-5:-3], key=lambda x: x.high)
    high_2 = rates[-4].high
    high_3 = rates[-3].high
    low_2 = rates[-2].low
    low_3 = rates[-1].low

    return high_2 > highest_high.high and high_3 == highest_high.high and low_2 > low_3

# Function to check for a double bottom pattern
def is_double_bottom(rates):
    if len(rates) < 5:
        return False

    lowest_low = min(rates[-5:-3], key=lambda x: x.low)
    low_2 = rates[-4].low
    low_3 = rates[-3].low
    high_2 = rates[-2].high
    high_3 = rates[-1].high

    return low_2 < lowest_low.low and low_3 == lowest_low.low and high_2 < high_3

# Function to check for a Head and Shoulders pattern
def is_head_and_shoulders(rates):
    if len(rates) < 7:
        return False

    high_1 = rates[-7].high
    high_2 = rates[-6].high
    high_3 = rates[-5].high
    low_1 = rates[-7].low
    low_2 = rates[-6].low
    low_3 = rates[-5].low
    neckline_low = min(low_2, low_3)
    neckline_high = max(high_2, high_3)
    shoulder_high = max(high_1, high_3)
    shoulder_low = min(low_1, low_3)

    return (
        high_1 > shoulder_high and
        high_2 > shoulder_high and
        high_3 > shoulder_high and
        low_1 > neckline_low and
        low_2 > neckline_low and
        low_3 > neckline_low and
        shoulder_high > neckline_high and
        shoulder_low > neckline_low
    )

# Function to check for an Inverse Head and Shoulders pattern
def is_inverse_head_and_shoulders(rates):
    if len(rates) < 7:
        return False

    low_1 = rates[-7].low
    low_2 = rates[-6].low
    low_3 = rates[-5].low
    high_1 = rates[-7].high
    high_2 = rates[-6].high
    high_3 = rates[-5].high
    neckline_low = max(high_2, high_3)
    neckline_high = min(low_2, low_3)
    shoulder_low = min(low_1, low_3)
    shoulder_high = max(high_1, high_3)

    return (
        low_1 < shoulder_low and
        low_2 < shoulder_low and
        low_3 < shoulder_low and
        high_1 < neckline_high and
        high_2 < neckline_high and
        high_3 < neckline_high and
        shoulder_low < neckline_low and
        shoulder_high < neckline_high
    )

# Function to check for a Wedge pattern
def is_wedge(rates):
    if len(rates) < 5:
        return False

    high_1 = rates[-5].high
    high_2 = rates[-4].high
    high_3 = rates[-3].high
    high_4 = rates[-2].high
    high_5 = rates[-1].high
    low_1 = rates[-5].low
    low_2 = rates[-4].low
    low_3 = rates[-3].low
    low_4 = rates[-2].low
    low_5 = rates[-1].low

    is_rising = (
        high_1 < high_2 < high_3 < high_4 < high_5 and
        low_1 < low_2 < low_3 < low_4 < low_5
    )

    is_falling = (
        high_1 > high_2 > high_3 > high_4 > high_5 and
        low_1 > low_2 > low_3 > low_4 > low_5
    )

    return is_rising or is_falling

# Function to check for a Rectangle pattern
def is_rectangle(rates):
    if len(rates) < 5:
        return False

    high_1 = rates[-5].high
    high_2 = rates[-4].high
    high_3 = rates[-3].high
    high_4 = rates[-2].high
    high_5 = rates[-1].high
    low_1 = rates[-5].low
    low_2 = rates[-4].low
    low_3 = rates[-3].low
    low_4 = rates[-2].low
    low_5 = rates[-1].low

    return (
        high_1 == high_2 == high_3 == high_4 == high_5 and
        low_1 == low_2 == low_3 == low_4 == low_5
    )

# Event handler for new bar/candlestick
def on_new_bar(symbol, timeframe, rates):
    # Check if the symbol and timeframe match our requirements
    if symbol == SYMBOL and timeframe == TIMEFRAME:
        if is_double_top(rates):
            # Place a sell trade for double top
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": 0.01,  # Specify your desired volume
                "type": mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(SYMBOL).bid,
                "slippage": 5,  # Specify your desired slippage
            }
            mt5.order_send(request)
            print("Double Top pattern detected. Placing sell trade.")
        elif is_double_bottom(rates):
            # Place a buy trade for double bottom
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": 0.01,  # Specify your desired volume
                "type": mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(SYMBOL).ask,
                "slippage": 5,  # Specify your desired slippage
            }
            mt5.order_send(request)
            print("Double Bottom pattern detected. Placing buy trade.")
        elif is_head_and_shoulders(rates):
            # Place a sell trade for head and shoulders
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": 0.01,  # Specify your desired volume
                "type": mt5.ORDER_TYPE_SELL,
                "price": mt5.symbol_info_tick(SYMBOL).bid,
                "slippage": 5,  # Specify your desired slippage
            }
            mt5.order_send(request)
            print("Head and Shoulders pattern detected. Placing sell trade.")
        elif is_inverse_head_and_shoulders(rates):
            # Place a buy trade for inverse head and shoulders
            request = {
                "action": mt5.TRADE_ACTION_DEAL,
                "symbol": SYMBOL,
                "volume": 0.01,  # Specify your desired volume
                "type": mt5.ORDER_TYPE_BUY,
                "price": mt5.symbol_info_tick(SYMBOL).ask,
                "slippage": 5,  # Specify your desired slippage
            }
            mt5.order_send(request)
            print("Inverse Head and Shoulders pattern detected. Placing buy trade.")
        elif is_wedge(rates):
            # Place a buy/sell trade for wedge pattern
            # Add your logic here based on the direction of the wedge pattern
            print("Wedge pattern detected.")
        elif is_rectangle(rates):
            # Place a buy/sell trade for rectangle pattern
            # Add your logic here based on the breakout direction of the rectangle pattern
            print("Rectangle pattern detected.")

# Connect to MT5 server
if not mt5.initialize():
    print("Failed to initialize MT5.")
    quit()

# Login to the account
if not mt5.login(LOGIN, PASSWORD):
    print("Failed to login to the account.")
    mt5.shutdown()
    quit()

# Subscribe to symbol's new bar events
mt5.symbol_select(SYMBOL, True)
mt5.copy_rates_from(SYMBOL, TIMEFRAME, 0, 1000)  # Adjust the number of bars to retrieve if needed
mt5.symbol_subscribe(SYMBOL, on_new_bar)

# Keep the program running
while mt5.connected():
    mt5.sleep(1000)

# Cleanup and disconnect
mt5.shutdown(
