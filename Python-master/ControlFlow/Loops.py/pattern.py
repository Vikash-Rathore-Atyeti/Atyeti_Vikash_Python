# print right-angled triangle
rows = int(input("Enter the number of rows: "))
for i in range(1, rows + 1):
    # Print spaces
    for j in range(rows - i):
        print(" ", end="")
    # Print asterisks
    for k in range(i):
        print("*", end="")
    # Move to the next line
    print()
