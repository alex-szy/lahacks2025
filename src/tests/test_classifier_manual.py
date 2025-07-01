import os
from classifier.classifier import Classifier
from utilities.file_system_config import FileSystemConfig
from models.file import File

def manual_test_classifier():
    # Setup: Add three folder paths
    config = FileSystemConfig()
    config.append_entry("/machine_learning", "Content related to machine learning topics, research, and implementations.")
    config.append_entry("/hobbies/cooking", "Recipes, cooking notes, and culinary experiments.")
    config.append_entry("/history/europe", "Documents related to world history, civilizations, and historical events.")

    # Initialize Classifier
    classifier = Classifier(token_threshold=10000)

    # Directory with files to classify
    resource_dir = "resources"
    files_to_test = [f for f in os.listdir(resource_dir) if os.path.isfile(os.path.join(resource_dir, f))]

    for filename in files_to_test:
        if filename == ".DS_Store":
            continue

        print(f"\n==== Working on {filename} ====")
        path = os.path.join(resource_dir, filename)
        with open(path, "rb") as f:
            content = f.read()

        file = File(content=content, name=filename, path=path)
        try:
            classified_path = classifier.classify(file)
            print(f"✅ {filename} classified as: {classified_path}")
        except Exception as e:
            print(f"❌ Error classifying {filename}: {e}")

if __name__ == "__main__":
    manual_test_classifier()
