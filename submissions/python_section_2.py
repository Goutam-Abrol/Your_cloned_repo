import pandas as pd

from datetime import time


def calculate_distance_matrix(file_path: str) -> pd.DataFrame:
    """
    Generate a DataFrame representing distances between IDs based on known routes.
    
    Args:
        file_path (str): The path to the CSV file containing distance data.
    
    Returns:
        pd.DataFrame: A DataFrame with cumulative distances between IDs.
    """
    
    df = pd.read_csv(file_path)
    
    
    unique_ids = pd.concat([df['id_start'], df['id_end']]).unique()
    

    distance_matrix = pd.DataFrame(0, index=unique_ids, columns=unique_ids)
    
    
    for _, row in df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']
        distance = row['distance']
        
        
        distance_matrix.at[id_start, id_end] = distance
        distance_matrix.at[id_start, id_end] = distance 
    
    
    for k in unique_ids:
        for i in unique_ids:
            for j in unique_ids:
                if distance_matrix.at[i, j] > 0:
                    continue  
                if distance_matrix.at[i, k] and distance_matrix.at[k, j]:
                    new_distance = distance_matrix.at[i, k] + distance_matrix.at[k, j]
                    if distance_matrix.at[i, j] == 0 or new_distance < distance_matrix.at[i, j]:
                        distance_matrix.at[i, j] = new_distance

    return distance_matrix


def unroll_distance_matrix(distance_matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll the distance matrix into a DataFrame with three columns: id_start, id_end, and distance.

    Args:
        distance_matrix (pd.DataFrame): The distance matrix with IDs as both index and columns.

    Returns:
        pd.DataFrame: A DataFrame with columns id_start, id_end, and distance.
    """
    
    results = []

    for id_start in distance_matrix.index:
        for id_end in distance_matrix.columns:
            if id_start != id_end:
                distance = distance_matrix.at[id_start, id_end]

                if distance > 0:
                    results.append((id_start, id_end, distance))

    unrolled_df = pd.DataFrame(results, columns=['id_start', 'id_end', 'distance'])

    return unrolled_df

def find_ids_within_ten_percentage_threshold(distance_df: pd.DataFrame, reference_id: int) -> list:
    """
    Find IDs within a 10% distance threshold of the average distance for a given reference ID.
    
    Args:
        distance_df (pd.DataFrame): DataFrame containing distances between IDs.
        reference_id (int): The ID for which to calculate the average distance.
    
    Returns:
        list: Sorted list of IDs within 10% of the average distance.
    """
    
    reference_distances = distance_df[distance_df['id_start'] == reference_id]['distance']
    
    if reference_distances.empty:
        print(f"No distances found for id_start {reference_id}.")
        return []
    
    average_distance = reference_distances.mean()
    
    lower_bound = average_distance * 0.9
    upper_bound = average_distance * 1.1
    
    filtered_ids = distance_df[(distance_df['id_start'] != reference_id) & 
                                (distance_df['distance'] >= lower_bound) & 
                                (distance_df['distance'] <= upper_bound)]
    
    unique_ids = filtered_ids['id_start'].unique()
    
    return sorted(unique_ids)


def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate toll rates based on vehicle types and distances.

    Args:
        df (pd.DataFrame): DataFrame containing distances between toll locations.

    Returns:
        pd.DataFrame: Updated DataFrame with added columns for each vehicle type.
    """
    rates = {
        'moto': 0.8,
        'car': 1.2,
        'rv': 1.5,
        'bus': 2.2,
        'truck': 3.6
    }
    
    for vehicle, rate in rates.items():
        df[vehicle] = df['distance'] * rate

    return df



def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame): DataFrame containing toll rates for different vehicle types.

    Returns:
        pandas.DataFrame: Updated DataFrame with added time-based columns and adjusted toll rates.
    """
    
    weekday_intervals = [
        (time(0, 0), time(10, 0), 0.8),    
        (time(10, 0), time(18, 0), 1.2),   
        (time(18, 0), time(23, 59, 59), 0.8) 
    ]
    
    weekend_discount = 0.7  

    results = []

    for index, row in df.iterrows():
        id_start = row['id_start']
        id_end = row['id_end']
        distance = row['distance']  

        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for start_time, end_time, discount in weekday_intervals:

                toll_rate_entry = {
                    'id_start': id_start,
                    'id_end': id_end,
                    'start_day': day,
                    'start_time': start_time,
                    'end_day': day,
                    'end_time': end_time,
                    'distance': distance,  
                    'moto': row['moto'] * discount,
                    'car': row['car'] * discount,
                    'rv': row['rv'] * discount,
                    'bus': row['bus'] * discount,
                    'truck': row['truck'] * discount
                }
                results.append(toll_rate_entry)
        
        for day in ['Saturday', 'Sunday']:
            toll_rate_entry = {
                'id_start': id_start,
                'id_end': id_end,
                'start_day': day,
                'start_time': time(0, 0),
                'end_day': day,
                'end_time': time(23, 59, 59),
                'distance': distance,  
                'moto': row['moto'] * weekend_discount,
                'car': row['car'] * weekend_discount,
                'rv': row['rv'] * weekend_discount,
                'bus': row['bus'] * weekend_discount,
                'truck': row['truck'] * weekend_discount
            }
            results.append(toll_rate_entry)

    
    final_df = pd.DataFrame(results)
    
    return final_df
