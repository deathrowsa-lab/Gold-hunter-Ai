import MetaTrader5 as mt5
import pandas as pd
import pandas_ta as ta
import threading
import time
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 1. Load Environment Variables (Login Info)
load_dotenv()
MT5_ACCOUNT = int(os.getenv("MT5_ACCOUNT", 0))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")

app = Flask(__name__)
CORS(app)

# Global toggle to turn bot ON/OFF from your app
BOT_ACTIVE = True

# --- TRADING LOGIC ---

def place_market_order(symbol, volume, order_type):
    """Executes a trade on MT5"""
    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        return None
    
    price = tick.ask if order_type == mt5.ORDER_TYPE_BUY else tick.bid
    
    # Simple SL/TP (e.g., 200 points)
    sl = price - 0.50 if order_type == mt5.ORDER_TYPE_BUY else price + 0.50
    tp = price + 1.00 if order_type == mt5.ORDER_TYPE_BUY else price - 1.00

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": float(volume),
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "magic": 1001,
        "comment": "Gold Hunter Auto",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    return mt5.order_send(request)

def auto_trade_cycle():
    """The 'Brain' that runs every minute"""
    symbol = "XAUUSD"
    lot = 0.01

    # 1. Get Data
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M15, 0, 200)
    if rates is None:
        return "MT5 Data Error"

    df = pd.DataFrame(rates)
    
    # 2. Indicators
    df['ema_200'] = ta.ema(df['close'], length=200)
    df['rsi'] = ta.rsi(df['close'], length=14)
    
    last_row = df.iloc[-1]
    prev_row = df.iloc[-2]

    # 3. Check for existing trades
    if len(mt5.positions_get(symbol=symbol)) > 0:
        return "Position already open"

    # 4. Strategy Check
    # BUY: Price > EMA200 and RSI crosses 30
    if last_row['close'] > last_row['ema_200'] and prev_row['rsi'] < 30 and last_row['rsi'] >= 30:
        place_market_order(symbol, lot, mt5.ORDER_TYPE_BUY)
        return "BUY Order Placed"

    # SELL: Price < EMA200 and RSI crosses 70
    if last_row['close'] < last_row['ema_200'] and prev_row['rsi'] > 70 and last_row['rsi'] <= 70:
        place_market_order(symbol, lot, mt5.ORDER_TYPE_SELL)
        return "SELL Order Placed"

    return "Market Scanned: No Signal"

def bot_loop():
    """Background loop that keeps the bot alive"""
    while True:
        if BOT_ACTIVE:
            try:
                print(auto_trade_cycle())
            except Exception as e:
                print(f"Loop Error: {e}")
        time.sleep(60) # Wait 1 minute

# --- FLASK API ROUTES ---

@app.route('/')
def home():
    return jsonify({"status": "Gold Hunter API Online"})

@app.route('/toggle', methods=['POST'])
def toggle_bot():
    global BOT_ACTIVE
    data = request.json
    BOT_ACTIVE = data.get("active", False)
    return jsonify({"bot_status": BOT_ACTIVE})

@app.route('/account', methods=['GET'])
def account_info():
    info = mt5.account_info()
    return jsonify(info._asdict()) if info else {"error": "Could not get info"}

# --- STARTING THE APP ---

if __name__ == "__main__":
    # Initialize MT5
    if not mt5.initialize(login=MT5_ACCOUNT, password=MT5_PASSWORD, server=MT5_SERVER):
        print("MT5 Initialization Failed")
    else:
        # Start the trading thread
        threading.Thread(target=bot_loop, daemon=True).start()
        # Start the Flask Web Server
        app.run(host='0.0.0.0', port=5000)
    
