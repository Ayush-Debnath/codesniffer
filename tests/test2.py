def bad_func(a, b, c, d, e, f):
    for i in range(10):
        if i % 2 == 0:
            for j in range(5):
                if j > 2:
                    for k in range(3):
                        print(i, j, k)