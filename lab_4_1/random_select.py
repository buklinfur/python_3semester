import argparse
import numpy as np
rng = np.random.default_rng()

def check_prob(prob):
    if prob > 1 or prob < 0:
        raise 'Probability must be between 0 and 1'

def read_data(filename):
    fin = open(filename)
    data = fin.readline()
    return np.array(data.split())

# 1
def data_injection1(real, synth, prob):
    indices = np.random.randint(0, real.size, size = rng.binomial(real.size, prob))
    result = real.copy()
    result [indices] = synth[indices]
    return result
# 2
def data_injection2(real, synth, prob):
    cond = rng.choice([True, False], real.size, p=[1-prob,prob])
    result = np.where(cond, real, synth)
    return result

def process_data(real_path, synthetic_path, prob):
    try:
        data = read_data(real_path)
        synthetic_data = read_data(synthetic_path)
    except Exception as e:
        print(f"Unable to read data:")
        raise e

    try:
        result1 = data_injection1(data, synthetic_data, prob)
    except Exception as e:
        print(f"Unable to inject data (way 1):")
        raise e

    print(f"Injection result 1:\n{' '.join(result1)}")

    try:
        result2 = data_injection2(data, synthetic_data, prob)
    except Exception as e:
        print(f"Unable to inject data (way 2):")
        raise e

    print(f"Injection result 2:\n{' '.join(result2)}")


def main() -> None:
    parser = argparse.ArgumentParser('Random select')
    parser.add_argument('realDataPath', type=str, help='path to real data file')
    parser.add_argument('syntheticDataPath', type=str, help='path to synthetic data file')
    parser.add_argument('probability', type=float, help='probability of selecting a real data')

    args = parser.parse_args()

    check_prob(args.probability)
    process_data(args.realDataPath, args.syntheticDataPath, args.probability)

main()