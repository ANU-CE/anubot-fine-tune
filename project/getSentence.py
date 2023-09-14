import csv
import os

def read_csv(file_name):
    data = []

    with open(file_name, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            data.append(row)

    return data

def convert_to_sentences(data):
    sentences = []

    for info in data:
        if(info[4] == 'False'):
            continue

        sentence = f"{info[1]} / {info[2]} / {info[3]} / 의 전화번호는 054-820-{info[4]}입니다."
        sentences.append(sentence)

    return sentences

def write_csv(output_file_name, sentences):
    with open(output_file_name, 'w', encoding='utf-8', newline='') as file:
        csv_writer = csv.writer(file)
        for sentence in sentences:
            csv_writer.writerow([sentence])

def main():
    fileName = "anubot_numb.csv"
    input_file_name = os.path.join(os.path.dirname(__file__), fileName)
    output_file_name = "output.csv"

    data = read_csv(input_file_name)
    sentences = convert_to_sentences(data)
    write_csv(output_file_name, sentences)

if __name__ == '__main__':
    main()
