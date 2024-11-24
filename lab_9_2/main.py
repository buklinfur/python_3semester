from ModelTester import ModelTester


def main():
    file_name = 'titanic_prepared.csv'
    categorical_columns = ['sex']
    target_column = 'label'

    tester = ModelTester(categorical_columns, file_name, target_column)

    decision_tree_accuracy = tester.test_decision_tree_accuracy()
    print(f'Decision tree accuracy: {decision_tree_accuracy:.3f}')

    random_forest_accuracy = tester.test_my_random_forest()
    print(f'My random forest accuracy: {random_forest_accuracy:.3f}')


main()