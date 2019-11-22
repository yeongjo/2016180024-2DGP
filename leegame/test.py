import copy as cp
def hi():
    a = input().split()
    b = [[], [], []]
    for i in range(3):
        for j in range(int(a[i])):
            b[i].append(int(input()))

    word_idx = [0, 0, 0]
    same_count = [0, 0, 0]

    compare_order = [[0, 1], [1, 2], [0, 2]]

    loop = True
    while loop:
        prev_same_count = cp.copy(same_count)
        for idx in range(3):
            compare_idx1 = compare_order[idx][0]
            compare_idx2 = compare_order[idx][1]
            word_idx1 = word_idx[compare_idx1]
            word_idx2 = word_idx[compare_idx2]
            if b[compare_idx1][word_idx1] == b[compare_idx2][word_idx2]:
                same_count[compare_idx1] = prev_same_count[compare_idx1] + 1
                same_count[compare_idx2] = prev_same_count[compare_idx2] + 1

        min_number = min(b[0][word_idx[0]], b[1][word_idx[1]], b[2][word_idx[2]])
        for i in range(3):
            if min_number == b[i][word_idx[i]]:
                word_idx[i] += 1
                if word_idx[i] >= len(b[i]):
                    loop = False
                    break


    print(word_idx)
    print(same_count)


hi()
