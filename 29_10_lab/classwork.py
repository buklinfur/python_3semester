import pandas as pd

def read_table(file_path: str) -> pd.DataFrame:
    file = open(file_path, 'r', encoding='utf-8')
    dataframe = pd.read_csv(file, header=0, index_col=0)
    print(dataframe)
    dataframe.to_csv('input.csv')
    return dataframe

# Task 1
# Разделите данные Титаника (train.csv) на тренировочную, валидационную и тестовую часть.
# С помощью валидационной части подберите гиперпараметры для моделей Random Forest, XGBoost,
# Logistic Regression и KNN. Получите точность этих моделей на тестовой части.



# Task 2
# С помощью RandomForest выберите 2, 4, 8 самых важных признаков и проверьте точность моделей
# только на этих признаках.


# function calls

def main():
    df = read_table('train.csv')
    print (df)
    df.to_csv('result.csv')

main()