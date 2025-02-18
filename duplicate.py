def find_duplicates(file_names=None, file_name='file_names.txt'):
    """
    Identifies duplicate file names from the given file or list and returns a list of duplicates.

    Args:
    file_names (list): A list of file names to check for duplicates. Default is None.
    file_name (str): The name of the file containing the list of file names. Default is 'file_names.txt'.

    Returns:
    dict: A dictionary where the keys are the duplicate file names and the values are lists of occurrences.
    """
    # If file_names list is not provided, read file names from the given file
    if file_names is None:
        with open(file_name, 'r') as file:
            file_names = [line.strip() for line in file.readlines()]

    # Create a dictionary to count occurrences of each file name
    file_count = {}
    for file in file_names:
        file_count[file] = file_count.get(file, 0) + 1

    # Filter out files that have more than one occurrence (duplicates)
    duplicates = {file: count for file, count in file_count.items() if count > 1}

    
    return duplicates
