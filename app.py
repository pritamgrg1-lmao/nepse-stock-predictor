from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import numpy as np
from io import StringIO
import os

app = Flask(__name__)
CORS(app)

class StockPredictor:
    """NEPSE Stock Price Predictor using technical analysis"""
    
    def __init__(self):
        self.predictions = []
    
    def calculate_technical_indicators(self, df):
        """Calculate technical indicators for stock data"""
        try:
            # Standardize column names
            column_mapping = {
                'LTP': 'Close',
                'Close Price': 'Close',
                'Open Price': 'Open',
                'High Price': 'High',
                'Low Price': 'Low',
                'Total Traded Quantity': 'Volume',
                'S.N.': 'Symbol'
            }
            df = df.rename(columns=column_mapping)
            
            # Ensure numeric columns
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # Fill missing values
            if 'Open' not in df.columns or df['Open'].isna().all():
                df['Open'] = df['Close']
            if 'High' not in df.columns or df['High'].isna().all():
                df['High'] = df['Close']
            if 'Low' not in df.columns or df['Low'].isna().all():
                df['Low'] = df['Close']
            if 'Volume' not in df.columns:
                df['Volume'] = 0
            
            # Calculate indicators
            df['PriceChange'] = df['Close'] - df['Open']
            df['PriceChangePercent'] = (df['PriceChange'] / df['Open']) * 100
            df['PriceChangePercent'] = df['PriceChangePercent'].fillna(0)
            
            # Simple Moving Average (5-day)
            df['SMA5'] = df['Close'].rolling(window=5, min_periods=1).mean()
            
            # Volatility
            df['Volatility'] = df['High'] - df['Low']
            df['VolatilityPercent'] = (df['Volatility'] / df['Close']) * 100
            df['VolatilityPercent'] = df['VolatilityPercent'].fillna(0)
            
            # RSI (Relative Strength Index) - 14 period
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            df['RSI'] = df['RSI'].fillna(50)
            
            return df
            
        except Exception as e:
            print(f"Error calculating indicators: {e}")
            return df
    
    def predict_signal(self, day1_df, day2_df, day3_df):
        """Generate buy/sell/hold signals based on 3 days of data"""
        predictions = []
        
        # Process each dataframe
        day1_df = self.calculate_technical_indicators(day1_df)
        day2_df = self.calculate_technical_indicators(day2_df)
        day3_df = self.calculate_technical_indicators(day3_df)
        
        # Get unique symbols from day 3 (most recent)
        symbols = day3_df['Symbol'].unique()
        
        for symbol in symbols:
            try:
                # Get data for this symbol across all 3 days
                d1 = day1_df[day1_df['Symbol'] == symbol]
                d2 = day2_df[day2_df['Symbol'] == symbol]
                d3 = day3_df[day3_df['Symbol'] == symbol]
                
                if d3.empty:
                    continue
                
                score = 0
                confidence = 0
                factors = []
                
                # Get latest values
                current_price = float(d3['Close'].iloc[-1])
                current_change = float(d3['PriceChangePercent'].iloc[-1])
                current_volume = float(d3['Volume'].iloc[-1])
                current_rsi = float(d3['RSI'].iloc[-1])
                
                # Factor 1: 3-day price trend
                if not d1.empty and not d2.empty:
                    day1_price = float(d1['Close'].iloc[-1])
                    trend = ((current_price - day1_price) / day1_price) * 100
                    
                    if trend > 5:
                        score += 3
                        factors.append(f"Strong 3-day uptrend: +{trend:.2f}%")
                    elif trend > 2:
                        score += 2
                        factors.append(f"Uptrend: +{trend:.2f}%")
                    elif trend > 0:
                        score += 1
                        factors.append(f"Slight uptrend: +{trend:.2f}%")
                    elif trend < -5:
                        score -= 3
                        factors.append(f"Strong 3-day downtrend: {trend:.2f}%")
                    elif trend < -2:
                        score -= 2
                        factors.append(f"Downtrend: {trend:.2f}%")
                    elif trend < 0:
                        score -= 1
                        factors.append(f"Slight downtrend: {trend:.2f}%")
                    confidence += 30
                
                # Factor 2: Recent momentum (day 3)
                if current_change > 4:
                    score += 2
                    factors.append(f"Strong recent gain: +{current_change:.2f}%")
                elif current_change > 1:
                    score += 1
                    factors.append(f"Recent gain: +{current_change:.2f}%")
                elif current_change < -4:
                    score -= 2
                    factors.append(f"Strong recent loss: {current_change:.2f}%")
                elif current_change < -1:
                    score -= 1
                    factors.append(f"Recent loss: {current_change:.2f}%")
                else:
                    factors.append(f"Minimal change: {current_change:.2f}%")
                confidence += 25
                
                # Factor 3: RSI (Relative Strength Index)
                if current_rsi > 70:
                    score -= 1
                    factors.append(f"Overbought (RSI: {current_rsi:.1f})")
                elif current_rsi < 30:
                    score += 1
                    factors.append(f"Oversold (RSI: {current_rsi:.1f})")
                else:
                    factors.append(f"Neutral RSI: {current_rsi:.1f}")
                confidence += 20
                
                # Factor 4: Volume trend
                if not d2.empty:
                    prev_volume = float(d2['Volume'].iloc[-1])
                    if prev_volume > 0:
                        volume_change = ((current_volume - prev_volume) / prev_volume) * 100
                        
                        if volume_change > 50 and current_change > 0:
                            score += 2
                            factors.append(f"High volume with price increase (+{volume_change:.1f}%)")
                        elif volume_change > 20 and current_change > 0:
                            score += 1
                            factors.append(f"Rising volume with price increase")
                        elif volume_change < -30 and current_change < 0:
                            score -= 1
                            factors.append(f"Low volume with price decrease")
                        confidence += 15
                
                # Factor 5: SMA comparison
                current_sma = float(d3['SMA5'].iloc[-1])
                if current_price > current_sma * 1.02:
                    score += 1
                    factors.append(f"Price above 5-day SMA (Rs. {current_sma:.2f})")
                elif current_price < current_sma * 0.98:
                    score -= 1
                    factors.append(f"Price below 5-day SMA (Rs. {current_sma:.2f})")
                else:
                    factors.append(f"Price near 5-day SMA")
                confidence += 10
                
                # Determine signal
                if score >= 4:
                    signal = 'STRONG BUY'
                    signal_color = 'success'
                elif score >= 2:
                    signal = 'BUY'
                    signal_color = 'success'
                elif score <= -4:
                    signal = 'STRONG SELL'
                    signal_color = 'danger'
                elif score <= -2:
                    signal = 'SELL'
                    signal_color = 'danger'
                else:
                    signal = 'HOLD'
                    signal_color = 'warning'
                
                predictions.append({
                    'symbol': symbol,
                    'signal': signal,
                    'signalColor': signal_color,
                    'currentPrice': round(current_price, 2),
                    'priceChange': round(current_change, 2),
                    'score': score,
                    'confidence': min(100, max(0, confidence)),
                    'factors': factors,
                    'rsi': round(current_rsi, 1),
                    'volume': int(current_volume)
                })
                
            except Exception as e:
                print(f"Error processing {symbol}: {e}")
                continue
        
        # Sort by signal priority and confidence
        signal_priority = {'STRONG BUY': 0, 'BUY': 1, 'HOLD': 2, 'SELL': 3, 'STRONG SELL': 4}
        predictions.sort(key=lambda x: (signal_priority.get(x['signal'], 5), -x['confidence']))
        
        return predictions

predictor = StockPredictor()

@app.route('/')
def index():
    """Serve the frontend HTML"""
    return render_template('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint to process CSV files and generate predictions"""
    try:
        # Check if files are present
        if 'day1' not in request.files or 'day2' not in request.files or 'day3' not in request.files:
            return jsonify({'error': 'Please upload all 3 CSV files'}), 400
        
        # Read CSV files
        day1_file = request.files['day1']
        day2_file = request.files['day2']
        day3_file = request.files['day3']
        
        # Parse CSV data
        day1_df = pd.read_csv(day1_file)
        day2_df = pd.read_csv(day2_file)
        day3_df = pd.read_csv(day3_file)
        
        # Generate predictions
        predictions = predictor.predict_signal(day1_df, day2_df, day3_df)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'total': len(predictions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'NEPSE Stock Predictor API is running'})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)