import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def load_data(filename='army_lists.json'):
    """Load the JSON data into a pandas DataFrame."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        
        # Convert date strings to datetime if they exist
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            df['Month'] = df['Date'].dt.strftime('%Y-%m')
        
        return df
    except FileNotFoundError:
        print(f"Error: {filename} not found. Please run the scraper first.")
        return None
    except json.JSONDecodeError:
        print(f"Error: {filename} is not valid JSON.")
        return None

def create_detachment_visualizations(df):
    """Create visualizations focusing on detachment performance."""
    # Set style
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Create figure with subplots
    fig = plt.figure(figsize=(20, 15))
    
    # 1. Detachment Usage Over Time
    plt.subplot(2, 2, 1)
    if 'Month' in df.columns and 'Detachment' in df.columns:
        monthly_detachments = df.groupby(['Month', 'Detachment']).size().unstack(fill_value=0)
        monthly_detachments.plot(marker='o', linewidth=2)
        plt.title('Detachment Usage Over Time', pad=20, fontsize=12)
        plt.xlabel('Month', fontsize=10)
        plt.ylabel('Number of Lists', fontsize=10)
        plt.xticks(rotation=45)
        plt.legend(title='Detachment', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True, alpha=0.3)
    
    # 2. Win Rate by Detachment
    plt.subplot(2, 2, 2)
    if 'Result' in df.columns and 'Detachment' in df.columns:
        win_rates = df.groupby('Detachment')['Result'].apply(
            lambda x: (x == 'Win').mean()
        ).sort_values(ascending=False)
        
        # Create bar plot with custom colors
        colors = sns.color_palette("husl", len(win_rates))
        win_rates.plot(kind='bar', color=colors)
        plt.title('Win Rate by Detachment', pad=20, fontsize=12)
        plt.xlabel('Detachment', fontsize=10)
        plt.ylabel('Win Rate', fontsize=10)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        # Add win rate percentages on top of bars
        for i, v in enumerate(win_rates):
            plt.text(i, v, f'{v:.1%}', ha='center', va='bottom')
    
    # 3. Average Points by Detachment
    plt.subplot(2, 2, 3)
    if 'Points' in df.columns and 'Detachment' in df.columns:
        avg_points = df.groupby('Detachment')['Points'].mean().sort_values(ascending=False)
        colors = sns.color_palette("husl", len(avg_points))
        avg_points.plot(kind='bar', color=colors)
        plt.title('Average Points by Detachment', pad=20, fontsize=12)
        plt.xlabel('Detachment', fontsize=10)
        plt.ylabel('Average Points', fontsize=10)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        # Add point values on top of bars
        for i, v in enumerate(avg_points):
            plt.text(i, v, f'{v:.1f}', ha='center', va='bottom')
    
    # 4. Detachment Popularity vs Win Rate
    plt.subplot(2, 2, 4)
    if 'Result' in df.columns and 'Detachment' in df.columns:
        popularity = df['Detachment'].value_counts()
        win_rates = df.groupby('Detachment')['Result'].apply(
            lambda x: (x == 'Win').mean()
        )
        
        # Create scatter plot
        plt.scatter(popularity, win_rates, s=100, alpha=0.6)
        
        # Add labels for each point
        for detachment in popularity.index:
            plt.annotate(
                detachment,
                (popularity[detachment], win_rates[detachment]),
                xytext=(5, 5),
                textcoords='offset points'
            )
        
        plt.title('Detachment Popularity vs Win Rate', pad=20, fontsize=12)
        plt.xlabel('Number of Lists', fontsize=10)
        plt.ylabel('Win Rate', fontsize=10)
        plt.grid(True, alpha=0.3)
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig('detachment_analysis.png', dpi=300, bbox_inches='tight')
    print("Detachment visualizations have been saved as 'detachment_analysis.png'")

def main():
    # Load the data
    df = load_data()
    if df is not None:
        print("\nDataset Summary:")
        print(f"Total entries: {len(df)}")
        print("\nColumns available:")
        for col in df.columns:
            print(f"- {col}")
        
        # Create detachment visualizations
        create_detachment_visualizations(df)
        
        # Print detachment statistics
        print("\nDetachment Statistics:")
        if 'Detachment' in df.columns:
            detachment_stats = df.groupby('Detachment').agg({
                'Result': lambda x: (x == 'Win').mean(),
                'Points': ['count', 'mean', 'std']
            }).round(3)
            print(detachment_stats)

if __name__ == "__main__":
    main() 