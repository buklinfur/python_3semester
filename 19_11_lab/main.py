from Model import Model


def show_precision_and_recall(precision: [float], recall: [float], name: str):
    precision_message = '\n'.join([f'Precision for {i} is {precision:.3f}' for i, precision in enumerate(precision)])
    print(precision_message)

    recall_message = '\n'.join([f'Recall for {i} is {recall:.3f}' for i, recall in enumerate(recall)])
    print(recall_message)

    total_precision = sum(precision) / len(precision)
    total_recall = sum(recall) / len(recall)
    print(f'\nTotal {name} precision: {total_precision:.3f}\nTotal {name} recall: {total_recall:.3f}')


def main():
    model = Model()

    precision, recall = model.get_accuracy(model.train)
    show_precision_and_recall(precision, recall, 'TRAIN')

    precision, recall = model.get_accuracy(model.test)

    show_precision_and_recall(precision, recall, 'TEST')


main()