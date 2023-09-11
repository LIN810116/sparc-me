import os
import json
import shutil
import openpyxl
import pandas as pd
from pathlib import Path

from xlrd import XLRDError



def check_row_exist(dataframe, unique_column, unique_value):
    """Check if a row exist with given unique value

    :param dataframe: metadata dataframe that must be checked
    :type dataframe: Pandas DataFrame
    :param unique_value: value that can be used to uniquely identifies a row
    :type unique_value: string
    :return: row index of the row identified with the unique value, or -1 if there is no row corresponding to the unique value
    :rtype: int
    :raises ValueError: if more than one row can be identified with given unique value
    """
    row_index = dataframe.index[dataframe[unique_column] == unique_value].tolist()
    if not row_index:
        row_index = -1
    elif len(row_index) > 1:
        error_msg = "More than one row can be identified with given unique value"
        raise ValueError(error_msg)
    else:
        row_index = row_index[0]
    return row_index


def convert_schema_excel_to_json(source_path, dest_path):
    wb = openpyxl.load_workbook(source_path)
    sheets = wb.sheetnames

    schema = dict()
    for sheet in sheets:
        schema[sheet] = dict()
        try:
            element_description = pd.read_excel(source_path, sheet_name=sheet)
        except XLRDError:
            element_description = pd.read_excel(source_path, sheet_name=sheet, engine='openpyxl')

        element_description = element_description.where(pd.notnull(element_description), None)

        for index, row in element_description.iterrows():
            element = row["Element"]
            schema[sheet][element] = dict()
            schema[sheet][element]["Required"] = row["Required"]
            schema[sheet][element]["Type"] = row["Type"]
            schema[sheet][element]["Description"] = row["Description"]
            schema[sheet][element]["Example"] = row["Example"]

    with open(dest_path, 'w') as f:
        json.dump(schema, f, indent=4)


def get_sub_folder_paths_in_folder(folder_path):
    """
    get sub folder paths in a folder
    :param folder_path: the parent folder path
    :type folder_path: str
    :return: list
    """
    folder = Path(folder_path)
    sub_folders = []
    for item in folder.iterdir():
        if item.is_dir():
            sub_folders.append(item)

    return sub_folders
