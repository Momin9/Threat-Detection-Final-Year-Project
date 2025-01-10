import pandas as pd
import numpy as np


def generate_synthetic_dataset():
    """
    Generates a synthetic dataset with:
    - 500,000 rows of data
    - 10 feature columns
    - 'threat' column as the target (0 for safe, 1 for threat)
    - Includes some rows with missing labels (-1) for semi-supervised learning
    """
    np.random.seed(42)
    data = []

    for _ in range(500000):
        # Generate 10 random features
        features = np.random.rand(10)

        # Randomly assign a 'threat' label with 5% probability of being a threat
        threat_label = np.random.choice([0, 1], p=[0.95, 0.05])

        # Introduce unlabeled data (-1) with 20% probability
        if np.random.rand() < 0.2:
            threat_label = -1  # Unlabeled data for semi-supervised learning

        data.append(np.append(features, threat_label))

    # Define column names
    columns = [f"feature_{i}" for i in range(10)] + ["threat"]

    # Convert the data into a Pandas DataFrame
    df = pd.DataFrame(data, columns=columns)

    # Save the dataset to a CSV file
    dataset_path = "synthetic_dataset.csv"
    df.to_csv(dataset_path, index=False)
    print(f"Synthetic dataset generated and saved to {dataset_path}")
    print(f"Dataset shape: {df.shape}")
    print("Preview of the dataset:")
    print(df.head())


if __name__ == "__main__":
    generate_synthetic_dataset()
