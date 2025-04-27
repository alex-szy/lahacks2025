def build_summarization_prompt(content: str, filename: str) -> str:
    prompt = (
        f"{SUMMARIZATION_PROMPT}"
        f"File Name: {filename}\n"
        f"File Content: {filename}\n"
    )
    return f"Summarize the following content briefly:\n\n{content}"

def build_classification_prompt(summary: str, filename: str, folder_paths: list[str], folder_descriptions: list[str]) -> str:
    
    folder_info = "\n".join(f"{path}: {desc}" for path, desc in zip(folder_paths, folder_descriptions))

    prompt = (
        f"{CLASSIFICATION_PROMPT}"
        f"Folders:\n{folder_info}\n\n"
        f"{CLASSIFICATION_EXAMPLES_SNIPPET}\n"
        f"Input:\nFilename: {filename}\nSummary: {summary}\nOutput:"
    )
    return prompt

def prepare_folder_info(config) -> tuple[list[str], list[str]]:
    entries = config.read_all_entries()
    folder_paths = list(entries.keys())
    folder_descriptions = [info["description"] for info in entries.values()]
    return folder_paths, folder_descriptions

SUMMARIZATION_PROMPT=\
"""
Summarize the following file in 300 words or less.

"""

CLASSIFICATION_PROMPT=\
"""
You will be given a file name and a summary of its contents.
Classify the file into exactly one of the following folders. 
If no folder matches appropriately, respond with PATH_NOT_FOUND.
Be quite liberal with the classification. PATH_NOT_FOUND should be used conservatively.

"""

CLASSIFICATION_EXAMPLES_SNIPPET=\
"""Here are a few Examples:
Example 1:
Input:
Filename: hw1_linked_lists.pdf
Summary: 
This document is the first homework assignment for CS101 (Introduction to Computer Science) Fall 2023. 
It focuses on implementing singly and doubly linked lists in C++. 
Students are required to write their own node and list classes, test insertion and deletion operations, and 
analyze time complexity for each major function. The assignment emphasizes understanding dynamic memory allocation 
and pointers, two key topics covered during weeks 2 and 3 of the course lectures. Additional practice problems and 
submission instructions are provided at the end of the document.
Folders:
/academics/fall2023/cs101/assignments: Assignments for CS101 course, Fall 2023.
/academics/fall2023/cs101/homeworks: Homework submissions for CS101 course, Fall 2023.
/academics/fall2023/math202/exams: Exam papers and solutions for Math202 course, Fall 2023.
/academics/fall2023/math202/homeworks: Homework submissions for Math202 course, Fall 2023.
/academics/spring2024/eng150/essays: Essay submissions for ENG150 course, Spring 2024.
/personal/notes/random: Miscellaneous personal notes not associated with any course or class.

Output:
/academics/fall2023/cs101/homeworks

Example 2:
Input:
Filename: eng150_final_essay.txt
Summary:
This is the final essay submission for ENG150 (English Literature) in Spring 2024. 
The essay critically analyzes the depiction of moral ambiguity in Joseph Conrad's *Heart of Darkness*. 
It explores themes of imperialism, the complexity of human nature, and narrative framing techniques. 
The student integrates textual evidence and references several academic critiques to argue that Conrad’s 
work challenges traditional notions of heroism and civilization. This essay fulfills the major paper requirement 
outlined in the course syllabus and was submitted ahead of the semester’s final deadline.
Folders:
/academics/fall2023/cs101/assignments: Assignments for CS101 course, Fall 2023.
/academics/fall2023/cs101/homeworks: Homework submissions for CS101 course, Fall 2023.
/academics/fall2023/math202/exams: Exam papers and solutions for Math202 course, Fall 2023.
/academics/fall2023/math202/homeworks: Homework submissions for Math202 course, Fall 2023.
/academics/spring2024/eng150/writings: Writing submissions for ENG150 course, Spring 2024.
/personal/notes/random: Miscellaneous personal notes not associated with any course or class.

Output:
/academics/spring2024/eng150/writings
"""
