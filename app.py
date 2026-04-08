from flask import Flask, request, jsonify
import MetaTrader5 as mt5

app = Flask(__name__)

@app.route('/trade', methods=['POST'])
def place_trade():
    data = request.json
    symbol = data.get("symbol", "XAUUSD") # Gold
    lot = data.get("lot", 0.01)
    
    # Logic to open a trade
    request_dict = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot,
        "type": mt5.ORDER_TYPE_BUY,
        "magic": 123456,
        "comment": "App Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    
    result = mt5.order_send(request_dict)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        return jsonify({"status": "error", "message": str(result.comment)}), 400
        
    return jsonify({"status": "success", "order_id": result.order})
    
    
