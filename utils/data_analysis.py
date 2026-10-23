import os
import matplotlib.pyplot as plt

def plot_class_distribution(dataset_path):

    class_counts = []

    classes = sorted(os.listdir(dataset_path))

    for cls in classes:
        class_folder = os.path.join(dataset_path, cls)
        if os.path.isdir(class_folder):
            count = len(os.listdir(class_folder))
            class_counts.append(count)

    plt.figure(figsize=(12,5))
    plt.bar(range(len(class_counts)), class_counts)
    plt.xlabel("Class Index")
    plt.ylabel("Number of Images")
    plt.title("Dataset Class Distribution")

    return plt
