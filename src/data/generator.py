import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_load_shedding_data(days=30):
    start_date = datetime.now() - timedelta(days=days)
    dates = [start_date + timedelta(hours=i) for i in range(days * 24)]
    
    # Simulate load shedding stages (0 to 6)
    # Higher probability of stages during evening peaks
    stages = []
    for dt in dates:
        if 17 <= dt.hour <= 21:
            stages.append(np.random.choice([2, 3, 4, 5, 6], p=[0.1, 0.2, 0.3, 0.3, 0.1]))
        else:
            stages.append(np.random.choice([0, 1, 2, 3], p=[0.4, 0.3, 0.2, 0.1]))
            
    df = pd.DataFrame({
        'timestamp': dates,
        'area': 'Cape Town',
        'stage': stages
    })
    
    df.to_csv('sample_data.csv', index=False)
    print(f"Generated {len(df)} rows of mock load shedding data.")

if __name__ == "__main__":
    generate_mock_load_shedding_data()
