import json
import os


data_root = '../data/microsoft'
files = ['draw.json', 'kushman.json', 'dolphin_t2_final.json']


def main():
    src = []
    tgt = []
    missed_datapoint = 0
    total_datapoints = 0
    for file in files:
        data = read_file(file)
        total_datapoints += len(data)
        for datapoint in data:
            try:
                qstn, sol = parse_datapoints(datapoint)
                src.append(qstn.strip())
                tgt.append(sol)
            except:
                missed_datapoint += 1
                continue
    print('missed {} datapoints among {}'.format(missed_datapoint, total_datapoints))
    write_data(src, tgt)


def read_file(file):
    with open(os.path.join(data_root, file)) as f:
        data = json.load(f)
    return data


def parse_datapoints(datapoint):
    if len(datapoint['lSolutions']) == 1:
        return datapoint['sQuestion'], datapoint['lSolutions'][0]
    return None


def write_data(src, tgt):
    with open(os.path.join(data_root, 'microsoft_src.txt'), 'w') as f:
        for item in src:
            f.write(item + '\n')

    with open(os.path.join(data_root, 'microsoft_tgt.txt'), 'w') as f:
        for item in tgt:
            f.write(str(item) + '\n')


if __name__ == '__main__':
    main()
