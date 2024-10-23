from typing import Dict, List, Any
import polyline
import pandas as pd
import haversine
from haversine import haversine, Unit 
from itertools import permutations



def reverse_by_n_elements(lst: List[int], n: int) -> List[int]:
    """
    Reverses the input list by groups of n elements.
    """
    
    # Your code goes here.
    for i in range(0, len(lst), n):
        lst[i:i+n] = lst[i:i+n][::-1]
    
    return lst


def group_by_length(lst: List[str]) -> Dict[int, List[str]]:
    length_groups = {}
    
    for string in lst:
        length = len(string)
        if length not in length_groups:
            length_groups[length] = []
        length_groups[length].append(string)

    
    dict= sorted((length_groups.items()))
    return dict

def flatten_dict(nested_dict: Dict[str, Any], parent_key: str = '', sep: str = '.') -> Dict[str, Any]:
    """
    Flattens a nested dictionary, including handling lists and using dot notation with list indices.
    
    :param nested_dict: The nested dictionary to flatten
    :param parent_key: The base key (used for recursive calls)
    :param sep: The separator to use between nested keys (default is '.')
    :return: A flattened dictionary
    """
    # Your code here
    flat_dict = {}

    def flatten(current_dict_or_list, parent_key):
        if isinstance(current_dict_or_list, Dict):
            # Traverse through dictionary items
            for key, value in current_dict_or_list.items():
                new_key = f"{parent_key}{sep}{key}" if parent_key else key
                flatten(value, new_key)
        elif isinstance(current_dict_or_list, list):
            # Traverse through list items
            for index, value in enumerate(current_dict_or_list):
                new_key = f"{parent_key}[{index}]"
                flatten(value, new_key)
        else:
            # Base case: Not a dict or list, so assign the value
            flat_dict[parent_key] = current_dict_or_list

    # Start flattening
    flatten(nested_dict, parent_key)
    dict=flat_dict
    
    return dict

def unique_permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list that may contain duplicates.
    
    :param nums: List of integers (may contain duplicates)
    :return: List of unique permutations
    """
    unique_permutations_set = set(permutations(nums))
    
    return [list(p) for p in unique_permutations_set]


def find_all_dates(text: str) -> List[str]:
    words = text.split()  
    valid_dates = []
    
    for word in words:
        word = word.strip(",.")  
       
        if is_valid_date(word):  
            valid_dates.append(word)
    
    return valid_dates 

def is_valid_date(date_str: str) -> bool:
    if '-' in date_str and date_str.count('-') == 2:
        day, month, year = date_str.split('-')
        if day.isdigit() and month.isdigit() and year.isdigit():
            day, month, year = int(day), int(month), int(year)
            return (1 <= month <= 12 and 1 <= day <= 31)

    elif '/' in date_str and date_str.count('/') == 2:
        month, day, year = date_str.split('/')
        if month.isdigit() and day.isdigit() and year.isdigit():
            month, day, year = int(month), int(day), int(year)
            return (1 <= month <= 12 and 1 <= day <= 31)

    elif '.' in date_str and date_str.count('.') == 2:
        year, month, day = date_str.split('.')
        if year.isdigit() and month.isdigit() and day.isdigit():
            month, day = int(month), int(day)
            return (1 <= month <= 12 and 1 <= day <= 31)

    return False

def polyline_to_dataframe(polyline_str: str) -> pd.DataFrame:
    
    decoded = polyline.decode(polyline_str)
    coordinates_list = list(decoded)

    
    df = pd.DataFrame(coordinates_list, columns=['latitude', 'longitude'])

    
    df['distance in METERS'] = 0.0

    for i in range(1, len(df)):
        coord1 = (df.loc[i-1, 'latitude'], df.loc[i-1, 'longitude'])
        coord2 = (df.loc[i, 'latitude'], df.loc[i, 'longitude'])
        df.loc[i, 'distance in METERS'] = haversine(coord1, coord2, unit=Unit.METERS)

    print("Decoded Coordinates with Distance:")
    print(df)
    return df



def rotate_and_multiply_matrix(matrix: List[List[int]]) -> List[List[int]]:
    """
    Rotate the given matrix by 90 degrees clockwise, then replace each element
    with the sum of all other elements in the same row and column (after rotation),
    excluding itself.
    
    Args:
    - matrix (List[List[int]]): 2D list representing the matrix to be transformed.
    
    Returns:
    - List[List[int]]: A new 2D list representing the transformed matrix.
    """
   # Your code here 
    n = len(matrix)

    # Step 1: Rotate the matrix by 90 degrees clockwise
    rotated_matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            rotated_matrix[j][n - 1 - i] = matrix[i][j]

    transformed_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            row_sum = sum(rotated_matrix[i]) - rotated_matrix[i][j]  
            col_sum = sum(rotated_matrix[k][j] for k in range(n)) - rotated_matrix[i][j]  
            transformed_matrix[i][j] = row_sum + col_sum

    return transformed_matrix


def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Verifies whether each (id, id_2) pair in the dataset covers a full 24-hour period 
    across all 7 days of the week (Monday to Sunday).

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series with multi-index (id, id_2) 
                   indicating False for correct timestamps and True for incomplete coverage.
    """
    
    def check_pair(group):
        
        unique_days = set(group['startDay']) | set(group['endDay'])
        
        
        all_days_covered = set(range(1, 8))  
        return unique_days != all_days_covered

    
    result = df.groupby(['id', 'id_2']).apply(check_pair)
    
    return result
