import random
import numpy as np

import torchvision
from torchvision.datasets import MNIST


class Model:
    @staticmethod
    def shape_data(data: MNIST) -> list:
        features = [np.reshape(x[0][0].numpy(), (784, 1)) for x in data]

        def vectorise(number: int):
            vec = np.zeros((10, 1))
            vec[number] = 1
            return vec.astype(float)

        labels = [vectorise(number=e[1]) for e in data]

        return list(zip(features, labels))

    def __init__(self):
        train_dataset = torchvision.datasets.MNIST(
            root="./MNIST/train", train=True,
            transform=torchvision.transforms.ToTensor(),
            download=True)

        test_dataset = torchvision.datasets.MNIST(
            root="./MNIST/test", train=False,
            transform=torchvision.transforms.ToTensor(),
            download=True)

        self.train = self.shape_data(train_dataset)
        self.test = self.shape_data(test_dataset)

        def average_digit(data: list, digit: int) -> np.ndarray:
            filtered_data = [x[0] for x in data if np.argmax(x[1]) == digit]
            filtered_array = np.asarray(filtered_data)
            return np.average(filtered_array, axis=0)

        self.avg_digits = [average_digit(self.train, digit) for digit in range(10)]

        self.biases = random.choices(population=range(40, 70), k=10)  # idk

        self.weights = [np.transpose(self.avg_digits[num]) for num in range(10)]

    def _predict_if_digit(self, image, num):
        return np.dot(self.weights[num], image) - self.biases[num] >= 0

    def get_prediction_vec(self, image):
        vec = []

        for possible_digit in range(10):
            if self._predict_if_digit(image, possible_digit):
                return vec + [1] + (9 - possible_digit) * [0]

            vec.append(0)

        return vec

    def get_accuracy(self, data) -> ([float], [float]):
        true_positives_by_digit = [0] * 10
        false_positives_by_digit = [0] * 10
        false_negatives_by_digit = [0] * 10

        for image, label in data:
            def de_vectorise_label() -> int:
                return int(sum([pos * pred for pos, pred in enumerate(label)]))

            real_digit = de_vectorise_label()
            for possible_digit in range(10):
                should_be_positive = possible_digit == real_digit
                is_positive = self._predict_if_digit(image, possible_digit)
                if is_positive:
                    if should_be_positive:
                        true_positives_by_digit[real_digit] += 1
                    else:
                        false_positives_by_digit[real_digit] += 1
                else:
                    if should_be_positive:
                        false_negatives_by_digit[real_digit] += 1

        def precision(i: int) -> float:
            return true_positives_by_digit[i] / (true_positives_by_digit[i] + false_positives_by_digit[i])

        def recall(i: int) -> float:
            return true_positives_by_digit[i] / (true_positives_by_digit[i] + false_negatives_by_digit[i])

        return [precision(i) for i in range(10)], [recall(i) for i in range(10)]