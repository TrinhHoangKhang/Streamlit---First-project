import streamlit as st

def create_table(row, col, content=0):
    table = []
    for _ in range(row):
        table.append([content] * col)
    return table


def prepare_table(s1, s2):
    table = []
    traceback = []

    # Khởi tạo 2 bảng
    table = create_table(len(s2) + 1, len(s1) + 1)
    traceback = create_table(len(s2) + 1, len(s1) + 1, '')

    # Dòng đầu tiên của bảng sẽ là: 0, 1, 2, 3, 4, ...
    # Cột đầu tiên của bảng sẽ là: 0, 1, 2, 3, 4, ...
    for i in range(1, len(s2) + 1):
        table[i][0] = i
        traceback[i][0] = 'add'
    for j in range(1, len(s1) + 1):
        table[0][j] = j
        traceback[0][j] = 'del'

    return table, traceback

def find_levenshtein_distance(s1, s2):
    # Tạo một bảng có số hàng là len(s2) + 1, số cột là len(s1) + 1

    # Tạo thêm một bảng traceback để dò ngược lại đường sau khi chúng ta tính xong
    # Traceback[i][j] sẽ chứa 1 trong 2 giá trị: 'sub', 'add', 'del'. Chỉ ra trước
    # đó chúng ta đã thực hiện thao tác gì để đến được ô hiên tại
    table = []
    traceback = []

    table, traceback = prepare_table(s1, s2)

    # ========================================================================
    # Duyệt các ô và tính giá trị cho ô đó, đồng thời cập nhật traceback
    for i in range(1, len(s2) + 1):
        for j in range(1, len(s1) + 1):
            # Nếu sửa
            sub_cost = table[i - 1][j - 1]
            if s1[j - 1] != s2[i - 1]:
                sub_cost += 1

            # Nếu thêm
            add_cost = table[i - 1][j] + 1

            # Nếu xóa
            del_cost = table[i][j - 1] + 1

            table[i][j] = min(sub_cost, add_cost, del_cost)

            # Cập nhật traceback
            if table[i][j] == sub_cost:
                traceback[i][j] = 'sub'
            elif table[i][j] == add_cost:
                traceback[i][j] = 'add'
            else:
                traceback[i][j] = 'del'

    return table[-1][-1]


# This function prepare vocabs list that will be used to correct the input word

def prepare_vocabs(file_path):
    vocabs = []
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            vocabs.append(line.strip())

    return vocabs

def main():
    st.title('Word Correction using Levenshtein Distance')
    input_word = st.text_input('Word:')
    vocabs = prepare_vocabs(r'data\vocab.txt')

    distances = {}
    if st.button('Compute'):
        for word in vocabs:
            distances[word] = find_levenshtein_distance(
                input_word.lower(), word)
        distances = sorted(distances.items(), key=lambda x: x[1])
        st.write('Corrected word: ', distances[0][0])

    col1, col2 = st.columns(2)
    col1.write('Vocabs')
    col2.write('Distance')
    col1.write(vocabs)
    col2.write(dict(distances))


if __name__ == '__main__':
    main()
