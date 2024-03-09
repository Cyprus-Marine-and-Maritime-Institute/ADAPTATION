
def xlsx_to_csv():
    import pandas as pd
    import os

    # Get the current working directory
    cwd = os.getcwd()

    # Get the path to the xlsx files
    xlsx_path = cwd + '/SPGlobalShipDetails_xlsx/'

    # Get the path to the csv files
    csv_path = cwd + '/SPGlobalShipDetails_csv/'

    # Get the list of xlsx files
    xlsx_files = os.listdir(xlsx_path)

    # Loop through the xlsx files
    for xlsx_file in xlsx_files:
        # Get the name of the file
        file_name = xlsx_file.split('.')[0]

        # Read the xlsx file
        df = pd.read_excel(xlsx_path + xlsx_file)

        # Write the csv file
        df.to_csv(csv_path + file_name + '.csv', index=False)




if __name__ == '__main__':
    xlsx_to_csv()