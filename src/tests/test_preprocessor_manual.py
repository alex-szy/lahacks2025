import os

from engine.database import File
from engine.preprocessor import Preprocessor


def manual_test_preprocessing():
    resource_dir = "resources"
    files_to_test = [
        f
        for f in os.listdir(resource_dir)
        if os.path.isfile(os.path.join(resource_dir, f))
    ]

    preprocessor = Preprocessor(token_threshold=1000)

    for filename in files_to_test:
        if filename == ".DS_Store":
            continue
        print(f"==== Working on {filename} ====")
        path = os.path.join(resource_dir, filename)
        with open(path, "rb") as f:
            content = f.read()

        file = File(content=content, name=filename, path=path)
        processed = preprocessor.preprocess(file)

        print(f"==== Content of {filename} ====")
        print(processed[:500])  # Print first 500 characters only
        print("\n\n")
        print(f"==== Content of {filename} ====")


if __name__ == "__main__":
    manual_test_preprocessing()
