import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import make_column_transformer
from sklearn.model_selection import train_test_split

# Task 1
# Проведите извлечение признаков из wells_info_with_prod.csv
# (хоть один из столбцов с датой и категориальным признаком должен остаться).
# Целевой переменной будет Prod1Year

# Task 2
# Разбейте данные на train и test

# Task 3
# Отмасштабируйте train (в том числе целевую переменную)

# Task 4
# Используя модель масштабирования train отмасштабируйте test
# (использовать метод transform у той же модели масштабирования)

# Function call
def main():
    file_name = 'wells_info_with_prod.csv'
    numeric_feature_columns = ['LatWGS84', 'LonWGS84', 'BottomHoleLatitude', 'BottomHoleLongitude',
                               'LATERAL_LENGTH_BLEND', 'PROP_PER_FOOT', 'WATER_PER_FOOT']
    data_feature_columns = ['PermitDate', 'SpudDate', 'CompletionDate', 'FirstProductionDate']
    categorical_feature_columns = ['operatorNameIHS', 'formation', 'BasinName', 'StateName', 'CountyName']
    target_column = 'Prod1Year'

    feature_columns = numeric_feature_columns + data_feature_columns + categorical_feature_columns

    dataframe = pd.read_table(file_name, delimiter=',')

    target = dataframe[[target_column]]

    features = dataframe[feature_columns]

    for data_column in data_feature_columns:
        features.loc[:, data_column] = pd.to_numeric(pd.to_datetime(features[data_column]))

    transformer = make_column_transformer(
        (OneHotEncoder(), categorical_feature_columns),
        remainder='passthrough')
    transformed = transformer.fit_transform(features).toarray()
    feature_names = transformer.get_feature_names_out()
    features = pd.DataFrame(transformed, columns=feature_names)

    features_train, features_test, target_train, target_test = train_test_split(features, target, test_size=0.3)

    scaler = StandardScaler()
    features_train_scaled = pd.DataFrame(scaler.fit_transform(features_train, target_train))
    features_test_scaled = pd.DataFrame(scaler.transform(features_test))

    target_train_scaled = pd.DataFrame(scaler.fit_transform(target_train))
    target_test_scaled = pd.DataFrame(scaler.transform(target_test))

    features_train_scaled.to_csv('features_train_scaled.csv', sep=',', encoding='utf-8')
    features_test_scaled.to_csv('features_test_scaled.csv', sep=',', encoding='utf-8')

    target_train_scaled.to_csv('target_train_scaled.csv', sep=',', encoding='utf-8')
    target_test_scaled.to_csv('target_test_scaled.csv', sep=',', encoding='utf-8')

main()