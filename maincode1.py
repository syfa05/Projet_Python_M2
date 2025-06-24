import numpy as np
import matplotlib.pyplot as plt
"""

greeting = 'Welcome to Python Programming'
print("{} {}".format(greeting,"rahul"))
file =open("rapport.txt")
#print(file.read())
print(file.readline() )
print(file.readline() )
file.close()
"""
with open("test.txt", "r") as reader:
    texte = reader.read()
    reversed(texte)
    with open("test.txt", "w") as writer:
        for line in reversed(texte):
            writer.write(line)
# This code reads a file, reverses its content, and writes it back to the same file.
# It uses a context manager to handle file operations safely.
# The 'with' statement ensures that the file is properly closed after its suite finishes, even if an error is raised.
# The 'reversed' function is used to reverse the content of the file.   