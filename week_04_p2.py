import os

# Step 1: Choose an Application
# I choose an e-book as the application to implement the Hypertext Model. The e-book will have chapters and sections as nodes, allowing the user to navigate between them.

# Step 2: Define Nodes and Content
# I define the nodes as chapters and sections within each chapter. Each chapter will act as a "node" containing content, and nodes will be linked together.


chapters = {
    1: {
        "title": "Introduction",
        "content": "Welcome to this ebook. This is the introduction chapter.",
        "links": [2]  # Link to Chapter 1
    },
    2: {
        "title": "Chapter 1: Basics of Python",
        "content": "In this chapter, we discuss the basics of Python programming.",
        "links": [1, 3]  # Link to Introduction and Chapter 2
    },
    3: {
        "title": "Chapter 2: Data Structures",
        "content": "This chapter covers various data structures in Python.",
        "links": [2, 4]  # Link to Chapter 1 and Chapter 3
    },
    4: {
        "title": "Chapter 3: Object-Oriented Programming",
        "content": "This chapter explains object-oriented programming in Python.",
        "links": [3]  # Link to Chapter 2
    }
}


# Step 3: Create Links
# Links are created by specifying the available nodes users can navigate to.


# Step 4: Design User Interface
# The user interface is a simple command-line interaction. Users input commands to navigate between chapters. If they want to go back, they can type 'B'.
def display_chapter(chapter_id, previous_chapter=None):
    clear_screen()

    # Fetch current chapter details
    chapter = chapters[chapter_id]
    
    # Display chapter title and content
    print(f"\n--- {chapter['title']} ---")
    print(f"{chapter['content']}")
    print("\nWhere would you like to go next?\n")
    
    # Display available links to other chapters
    for link in chapter['links']:
        print(f"Type {link} to go to {chapters[link]['title']}")
    
    # If there's a previous chapter, offer a back option
    if previous_chapter:
        print("Type B to go back to the previous chapter")

    # Get user input for the next chapter to navigate to
    while True:
        choice = input("Enter your choice: ").strip().upper()
        if choice.isdigit() and int(choice) in chapter['links']:
            return int(choice)
        elif choice == 'B' and previous_chapter:
            return previous_chapter
        else:
            print("Invalid choice. Please try again.")

def clear_screen():
    os.system('cls')

# Step 5: Implement Hyperlinks
# In the `display_chapter()` function, I simulate hyperlinks by showing users options to navigate between chapters.

# Step 6: Test Navigation
# Now, let's test the navigation by allowing users to move between different chapters. The user starts at the "Introduction" node.


# Step 7: Enhance User Experience
def start_reading():
    current_chapter = 1 
    previous_chapter = None
    
    # Continue navigation until the user decides to stop
    while True:
        next_chapter = display_chapter(current_chapter, previous_chapter)  # Display the current chapter
        previous_chapter = current_chapter  # Update the previous chapter before moving on
        current_chapter = next_chapter  # Move to the next chapter selected by the user

# Step 7: Enhance User Experience
# The 'back' feature is also implemented, allowing users to return to the previous chapter.


# Step 8: Test and Debug
if __name__ == "__main__":
    start_reading()
