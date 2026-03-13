import csv
import random
from datetime import datetime, timedelta

def generate_sample_csv(filename, num_stocks=20, base_date=None):
    """Generate sample NEPSE stock data for testing"""
    
    if base_date is None:
        base_date = datetime.now()
    
    # Common NEPSE stock symbols
    symbols = [
        'NABIL', 'NIC', 'SCBNL', 'HBL', 'EBL', 'BOKL', 'NICA', 'MBL', 'NBL', 'SBI',
        'PRVU', 'GBIME', 'CZBIL', 'SANIMA', 'NCCB', 'SBL', 'KBL', 'MEGA', 'PCBL', 'ADBL',
        'HIDCL', 'NHPC', 'UPPER', 'API', 'CHCL', 'SHPC', 'NGPL', 'NLIC', 'NICL', 'PRIN'
    ]
    
    stocks_data = []
    
    for i in range(min(num_stocks, len(symbols))):
        symbol = symbols[i]
        
        # Generate base price (random between 200-2000)
        base_price = random.uniform(200, 2000)
        
        # Generate OHLC data
        open_price = round(base_price, 2)
        close_price = round(base_price * random.uniform(0.97, 1.03), 2)
        high_price = round(max(open_price, close_price) * random.uniform(1.00, 1.02), 2)
        low_price = round(min(open_price, close_price) * random.uniform(0.98, 1.00), 2)
        
        # Generate volume
        volume = random.randint(1000, 100000)
        
        stocks_data.append({
            'Symbol': symbol,
            'Open': open_price,
            'High': high_price,
            'Low': low_price,
            'Close': close_price,
            'Volume': volume
        })
    
    # Write to CSV
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for stock in stocks_data:
            writer.writerow(stock)
    
    print(f"Generated {filename} with {len(stocks_data)} stocks")

def generate_trending_data(symbol, base_price, trend='up', volatility=0.02):
    """Generate stock data with a specific trend"""
    if trend == 'up':
        change = random.uniform(0.01, 0.04)
        close = base_price * (1 + change)
    elif trend == 'down':
        change = random.uniform(0.01, 0.04)
        close = base_price * (1 - change)
    else:  # neutral
        change = random.uniform(-0.01, 0.01)
        close = base_price * (1 + change)
    
    open_price = round(base_price, 2)
    close_price = round(close, 2)
    high_price = round(max(open_price, close_price) * (1 + volatility), 2)
    low_price = round(min(open_price, close_price) * (1 - volatility), 2)
    volume = random.randint(5000, 80000)
    
    return {
        'Symbol': symbol,
        'Open': open_price,
        'High': high_price,
        'Low': low_price,
        'Close': close_price,
        'Volume': volume
    }

def generate_realistic_3day_data():
    """Generate 3 days of realistic trending data"""
    
    symbols = ['NABIL', 'NIC', 'SCBNL', 'HBL', 'EBL', 'BOKL', 'NICA', 'MBL', 'NBL', 'SBI']
    
    # Initialize base prices
    base_prices = {symbol: random.uniform(500, 1500) for symbol in symbols}
    
    # Day 1
    day1_data = []
    for symbol in symbols:
        trend = random.choice(['up', 'neutral', 'down'])
        stock_data = generate_trending_data(symbol, base_prices[symbol], trend)
        day1_data.append(stock_data)
        base_prices[symbol] = stock_data['Close']
    
    # Day 2 - continue trends
    day2_data = []
    for symbol in symbols:
        # 70% chance to continue trend, 30% to reverse
        if random.random() > 0.3:
            trend = 'up' if base_prices[symbol] > day1_data[symbols.index(symbol)]['Open'] else 'down'
        else:
            trend = random.choice(['up', 'neutral', 'down'])
        
        stock_data = generate_trending_data(symbol, base_prices[symbol], trend)
        day2_data.append(stock_data)
        base_prices[symbol] = stock_data['Close']
    
    # Day 3 - strengthen or weaken trends
    day3_data = []
    for symbol in symbols:
        # Check if stock is trending
        price_change = base_prices[symbol] - day1_data[symbols.index(symbol)]['Open']
        if price_change > 0:
            trend = 'up' if random.random() > 0.3 else 'neutral'
        elif price_change < 0:
            trend = 'down' if random.random() > 0.3 else 'neutral'
        else:
            trend = 'neutral'
        
        stock_data = generate_trending_data(symbol, base_prices[symbol], trend)
        day3_data.append(stock_data)
    
    # Write to CSV files
    for day_num, data in enumerate([day1_data, day2_data, day3_data], 1):
        filename = f'sample_day{day_num}.csv'
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for stock in data:
                writer.writerow(stock)
        print(f"Generated {filename}")

if __name__ == '__main__':
    print("Generating sample NEPSE stock data files...")
    print("-" * 50)
    
    # Generate realistic 3-day trending data
    generate_realistic_3day_data()
    
    print("-" * 50)
    print("Sample files generated successfully!")
    print("\nYou can now use these files to test the Stock Predictor:")
    print("  - sample_day1.csv (Day 1 - Oldest)")
    print("  - sample_day2.csv (Day 2 - Middle)")
    print("  - sample_day3.csv (Day 3 - Latest)")