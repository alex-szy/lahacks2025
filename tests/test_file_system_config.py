from pathlib import Path
from utilities.file_system_config import FileSystemConfig  # Adjust if needed based on your actual file/module name

def manual_test():
    cfg = FileSystemConfig()

    # Add a few entries
    cfg.append_entry("folder1/fileA.txt", "Description for file A in folder 1.")
    cfg.append_entry("folder2/fileB.txt", "Description for file B in folder 2.")
    cfg.append_entry("folder3/fileC.txt", "Description for file C in folder 3.")

    # Read all entries
    all_entries = cfg.read_all_entries()
    print("\nAll Entries:")
    for path, info in all_entries.items():
        print(f"Path: {path}, Info: {info}")

    # Read a specific entry
    specific_entry = cfg.read_entry("folder2/fileB.txt")
    print("\nSpecific Entry for 'folder2/fileB.txt':")
    print(specific_entry)

if __name__ == "__main__":
    manual_test()
