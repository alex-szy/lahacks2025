# 🐈 Munchkin 🐈: Semantic File Explorer/Organizer

Ever felt like your downloads folder is too cluttered and wished that there was a tool to automatically organize it? Dissatisfied with the current search functionality of your operating system?

Munchkin (`mckn`) offers a 2 pronged solution to your problems. It is comprised of 2 parts:

1. File sorting on download
2. Semantic file search

First, configure Munchkin with a list of folder **associations**. Essentially, you **associate** a folder with a particular semantic meaning, for example, a class on compilers and programming languages, or a particular topic you're interested in, like archeology.

Next, the `munchkin` server runs in the background and watches the folders you configure for new files. When a file appears in one of the folders, Munchkin takes a look at the file and automatically decides which (if any) of the preconfigured folder associations best matches the content of the file. It then automatically moves the file into the folder with that association, keeping your downloads folder clean.

Furthermore, each supported file seen by Munchkin also has its metadata stored in a local database. When you want to search for a file, Munchkin performs a lookup and finds the file which best matches your query. No more headaches looking for a file just because it has a strange name!

## System Architecture

![image](assets/munchkin_arch.png)

Our system is built on a highly modular architecture. The backend is structured like so:
- The `munchkin` server runs a set of observer threads
- The observer threads pass files along to the `saveprocessor`
- The `saveprocessor` orchestrates the preprocessing of the file, the classification of the file content and the saving of embeddings to the vector database
- The `queryprocessor` handles the semantic searching of files

`munchkin` has 2 frontends, a CLI and a GUI, which both communicate with the server through a clerk which is an abstraction over a lightweight HTTP API. Choose whichever frontend you're more comfortable with. Example usages are below:

```
mckn start                       # Start the daemon
mckn stop                        # Stop the daemon
mckn find <query>                # Find a file using a query string
mckn watch add ~/Downloads       # Add downloads folder to watch paths
mckn assoc add ~/Desktop/Biology # Add Biology folder to folder associations
mckn gui                         # Start the gui
...
```

![image](assets/munchkin_demo.png)

## Installation

We've packaged up munchkin to make the installation process as simple as possible. Using [`uv`](https://docs.astral.sh/uv/) will make the installation process a lot faster.

```
cd lahacks2025
pip install -e .    # with pip
uv sync             # with uv
```
