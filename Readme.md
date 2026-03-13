# NEPSE Stock Price Predictor

A complete stock prediction application for the Nepal Stock Exchange (NEPSE) using technical analysis and machine learning-based scoring.

## Features

- **Advanced Technical Analysis**: RSI, SMA, price trends, volatility, and volume analysis
- **Intelligent Signals**: BUY, STRONG BUY, HOLD, SELL, and STRONG SELL recommendations
- **Confidence Scoring**: Each prediction comes with a confidence percentage
- **Modern UI**: Beautiful, responsive Bootstrap 5 interface
- **Real-time Processing**: Fast CSV analysis with detailed factor breakdowns

## Technology Stack

### Backend (Python)
- **Flask**: Web framework
- **Pandas**: Data processing and analysis
- **NumPy**: Numerical computations
- **Flask-CORS**: Cross-origin resource sharing

### Frontend (HTML/CSS/JavaScript)
- **Bootstrap 5**: Modern, responsive UI
- **Bootstrap Icons**: Beautiful iconography
- **Vanilla JavaScript**: No framework dependencies

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project files**

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to: `http://localhost:5000`

## Usage Guide

### 1. Prepare Your Data
You need 3 CSV files containing NEPSE stock data for 3 consecutive trading days. Each CSV should have these columns:
- `Symbol` (or `S.N.`)
- `Open` (or `Open Price`)
- `High` (or `High Price`)
- `Low` (or `Low Price`)
- `Close` (or `LTP` or `Close Price`)
- `Volume` (or `Total Traded Quantity`)

Example CSV format:
```csv
Symbol,Open,High,Low,Close,Volume
NABIL,1250.00,1275.00,1240.00,1265.00,45000
NIC,850.50,865.00,845.00,860.00,32000
```

### 2. Upload Files
- Click on each upload area (Day 1, Day 2, Day 3)
- Select the corresponding CSV file
- Day 1 = Oldest, Day 3 = Most recent

### 3. Generate Predictions
- Click the "Generate Predictions" button
- Wait for analysis to complete (usually 1-3 seconds)
- View results with detailed analysis

### 4. Interpret Results

**Signal Types:**
- **STRONG BUY**: Score ≥ 4 - Strong upward indicators
- **BUY**: Score 2-3 - Positive momentum
- **HOLD**: Score -1 to 1 - Neutral, wait for clearer signals
- **SELL**: Score -3 to -2 - Negative momentum
- **STRONG SELL**: Score ≤ -4 - Strong downward indicators

**Confidence Score:**
- 70-100%: High confidence
- 50-69%: Moderate confidence
- Below 50%: Low confidence (use caution)

**Analysis Factors:**
Click "View Analysis Factors" on any stock to see:
- 3-day price trend
- Recent momentum
- RSI (Relative Strength Index)
- Volume trends
- SMA (Simple Moving Average) comparison

## How the Algorithm Works

### 1. Technical Indicators Calculation
- **Price Change**: Daily open-to-close movement
- **SMA (5-day)**: Simple moving average for trend detection
- **RSI**: Relative Strength Index for overbought/oversold conditions
- **Volatility**: High-low range analysis

### 2. Scoring System

The algorithm uses a multi-factor scoring system:

| Factor | Weight | Scoring Logic |
|--------|--------|--------------|
| 3-Day Trend | 30% | +3 to -3 points based on price movement |
| Recent Momentum | 25% | +2 to -2 points based on latest day change |
| RSI | 20% | +1 for oversold (<30), -1 for overbought (>70) |
| Volume Trend | 15% | +2 for high volume with price increase |
| SMA Position | 10% | +1 if price above SMA, -1 if below |

### 3. Signal Generation
- Total score determines the final signal
- Confidence is calculated based on data completeness and indicator strength

## API Endpoints

### POST `/api/predict`
Generate stock predictions from uploaded CSV files.

**Request:**
- Content-Type: `multipart/form-data`
- Form fields: `day1`, `day2`, `day3` (CSV files)

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "symbol": "NABIL",
      "signal": "BUY",
      "currentPrice": 1265.00,
      "priceChange": 1.5,
      "confidence": 75,
      "factors": ["Uptrend: +2.5%", "Price above SMA"],
      "rsi": 58.2,
      "volume": 45000
    }
  ],
  "total": 150
}
```

### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "message": "NEPSE Stock Predictor API is running"
}
```

## Project Structure

```
nepse-stock-predictor/
│
├── app.py                  # Flask backend application
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Frontend HTML
└── README.md              # This file
```

## Customization

### Adjusting Algorithm Sensitivity

In `app.py`, you can modify the scoring thresholds:

```python
# Change signal thresholds
if score >= 4:      # Currently STRONG BUY
    signal = 'STRONG BUY'
elif score >= 2:    # Currently BUY
    signal = 'BUY'
```

### Adding More Indicators

You can add additional technical indicators in the `calculate_technical_indicators` method:

```python
# Example: Add MACD
df['EMA12'] = df['Close'].ewm(span=12).mean()
df['EMA26'] = df['Close'].ewm(span=26).mean()
df['MACD'] = df['EMA12'] - df['EMA26']
```

## Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
pip install -r requirements.txt --upgrade
```

**2. "Port already in use"**
Change the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**3. CSV parsing errors**
Ensure your CSV files:
- Are properly formatted (comma-separated)
- Have the correct column headers
- Don't have extra empty rows
- Use UTF-8 encoding

**4. Empty results**
Check that:
- All 3 files have data
- Symbol names match across files
- Numeric values are properly formatted

## Limitations & Disclaimer

⚠️ **IMPORTANT DISCLAIMER** ⚠️

This application is for **educational purposes only**. It is NOT:
- Financial advice
- A guarantee of future performance
- A substitute for professional investment guidance

**Limitations:**
- Based on historical data only
- Cannot predict external market events
- Simplified technical analysis
- No fundamental analysis included
- Does not account for market sentiment, news, or economic factors

**Always:**
- Do your own research
- Consult with licensed financial advisors
- Understand the risks before investing
- Never invest more than you can afford to lose

## Future Enhancements

Potential improvements:
- [ ] Machine learning model training
- [ ] More technical indicators (MACD, Bollinger Bands)
- [ ] Historical backtesting
- [ ] Real-time data integration
- [ ] Export results to PDF/Excel
- [ ] User authentication and saved predictions
- [ ] Mobile app version
- [ ] Email/SMS alerts for signals

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Ensure all dependencies are properly installed

## Credits

Created for NEPSE stock market analysis using Flask and Bootstrap.

---

**Remember:** Past performance does not guarantee future results. Always invest responsibly!