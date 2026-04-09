def Matrix(width, height):
    for y in range(height):
        for x in range(width):
            print(y*width + x)

Matrix(8,4)