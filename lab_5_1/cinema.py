import pandas as pd

def read_table(file_path: str) -> pd.DataFrame:
    file = open(file_path, 'r', encoding='utf-8')
    dataframe = pd.read_csv(file, delimiter=' ', header = 0, index_col=0)
    print(dataframe)
    return dataframe

def is_sex_defined(x):
    return x['sex'].lower() not in ['-', 'не указан']

def encode_sex_symbol(x):
    if x['sex'].lower() in ['m', 'м', 'мужчина']: return 1
    return 0

# function calls
def main ():
    titanic_with_labels = read_table('src/titanic_with_labels.csv')

    titanic_with_labels = titanic_with_labels[titanic_with_labels.apply(is_sex_defined, axis=1)]
    titanic_with_labels['sex'] = titanic_with_labels.apply(encode_sex_symbol, axis=1)

    max_row = titanic_with_labels['row_number'].max()
    no_row_indices = (titanic_with_labels['row_number'].isnull()) & (titanic_with_labels['row_number'] == '')
    titanic_with_labels[no_row_indices]['row_number'] = max_row

    high_quantile = titanic_with_labels["liters_drunk"].astype(float).quantile(0.90)

    adequate_drunk_rows = titanic_with_labels[
        titanic_with_labels.apply(lambda x: 0 <= float(x['liters_drunk']) < high_quantile, axis=1)]

    drunk_average = adequate_drunk_rows['liters_drunk'].astype(float).mean()

    def change_inadequate(x):
        return x['liters_drunk'] if 0 <= float(x['liters_drunk']) < high_quantile else drunk_average

    titanic_with_labels['liters_drunk'] = titanic_with_labels.apply(change_inadequate, axis=1)
    print(titanic_with_labels)

    cinema_sessions = read_table('src/cinema_sessions.csv')
    print(cinema_sessions)

main()