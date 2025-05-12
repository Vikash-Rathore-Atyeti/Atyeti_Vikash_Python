# print right-angled triangle
rows = int(input("Enter the number of rows: "))
for i in range(1, rows + 1):
    # Print spaces to align the stars to the right
    for j in range(rows - i):
        print(" ", end="")
    # Print asterisks for the current row
    for k in range(i):
        print("*", end="")
    # Move to the next line after printing each row
    print()
