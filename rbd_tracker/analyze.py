import json
import pandas as pd
import numpy as np
import argparse

from pathlib import Path 

from holoviews import opts
from bokeh.models.formatters import DatetimeTickFormatter

def main(
        sleep_data_json=Path('data/raw/dummy_data.json'), 
        out_file=Path('data/interim/dummy_data.parquet')
        ):

    # load the sleep data into a pandas dataframe
    with open(sleep_data_json) as f:
        sleep_data = json.load(f)

    print(f"opened {sleep_data_json} for processing")

    df_sleep = pd.DataFrame(sleep_data)

    # filter by long_sleep to get nighttime sleep
    df_sleep = df_sleep[df_sleep['type'] == 'long_sleep']

    # collate the sleep_phase and movement data in a nightly timescale
    collated_sleeps = []
    for i, row in df_sleep.iterrows():
        collated_sleeps.append(_collate_sleep(row))
    df_collated_sleeps = pd.concat(collated_sleeps)

    # `identify potential RBD events
    df_collated_sleeps.loc[(df_collated_sleeps['movement'] >= 3) & (df_collated_sleeps['sleep_phase'] == 3), 'RBD'] = df_collated_sleeps['movement'] + 0.5
    
    print('Potential RBD Events:')
    print(df_collated_sleeps.loc[(df_collated_sleeps['movement'] >= 3) & (df_collated_sleeps['sleep_phase'] == 3)][['movement', 'sleep_phase']])

    df_collated_sleeps.to_parquet(out_file)
    print(f"saved collated sleep data to {out_file}")

def _collate_sleep(row):
    
    # Convert the bedtime_start to a pandas datetime object
    bedtime_start = pd.to_datetime(row['bedtime_start'])

    # Extract the movement and sleep phase data
    movement_30_sec = [int(s) for s in list(row['movement_30_sec'])]
    sleep_phase_5_min = [int(s) for s in list(row['sleep_phase_5_min'])]

    # Create a pandas timeseries with 30-second intervals
    timeseries_30_sec = pd.date_range(start=bedtime_start, periods=len(movement_30_sec), freq='30s')

    # Repeat the sleep phase data to match the new times array
    sleep_phase_30_sec = np.repeat(sleep_phase_5_min, (5 * 60) // 30)[:len(timeseries_30_sec)]

    # Create the resampled DataFrame
    df = pd.DataFrame({'time': timeseries_30_sec, 'movement': movement_30_sec, 'sleep_phase': sleep_phase_30_sec})
    df.loc[:,'day'] = row['day']
    df.set_index(['day', 'time'], inplace=True)

    print(f'parsed {row["day"]}')
    
    return df


def plot_collated_sleep(df):
    '''Make a plot of the sleep phase and movement data, with potential RBD events highlighted'''

    # Create a DatetimeTickFormatter with the desired format
    formatter = DatetimeTickFormatter(hours='%H:%M', minutes='%H:%M')

    # Define the mapping of numerical values to text labels for sleep phases
    sleep_phase_labels = {
        1: 'Deep Sleep',
        2: 'Light Sleep',
        3: 'REM Sleep',
        4: 'Awake'
    }

    # Plot the line and scatter with a secondary y-axis
    line_plot = df.hvplot.line(x='time', y='sleep_phase', xformatter=formatter, label='Sleep Phase').opts(
        ylabel='Sleep Phase',
        yticks=[(k, v) for k, v in sleep_phase_labels.items()]
    )
    line_plot2 = df.hvplot.line(x='time', y='movement', xformatter=formatter, label='Movement').opts(
        ylabel='Movement', color='orange', line_width=.5
    )
    scatter_plot = df.hvplot.scatter(x='time', y='RBD', color='green', size=100, label='RBD Event?').opts(
        yaxis='right',
        ylabel='RBD'
    )

    # Combine the plots
    combined_plot = line_plot * line_plot2 * scatter_plot
    combined_plot.opts(
        opts.Overlay(
            yaxis='left',
            yformatter='%d'  # Adjust y-axis formatter if needed
        )
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process sleep data JSON file.')
    parser.add_argument('-i', '--sleep_data_json', type=str, help='Path to the sleep data JSON file', default='data/raw/dummy_data.json')
    parser.add_argument('-o', '--out_file', type=str, help='Path to the processed parquet file', default='data/interim/dummy_data.parquet')
    args = parser.parse_args()

    main(
        sleep_data_json=Path(args.sleep_data_json), 
        out_file=Path(args.out_file)
    )