import json
import heapq
import numpy as np
from collections import Counter


def get_probability(w):
    
    c = Counter(w)
    
    return {key: value / len(w) for key, value in c.items()}


def entropy(s):

    p = get_probability(s)
    
    return sum([-pi * np.log2(pi) for pi in p.values()])


def huffman_encoding(data):
    
    freq = get_probability(data)

    heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        for pair in left[1:]:
            pair[1] = '0' + pair[1]
        for pair in right[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [left[0] + right[0]] + left[1:] + right[1:])

    huffman_dict = dict(sorted(heapq.heappop(heap)[1:], key=lambda x: (len(x[-1]), x)))
    encoded_data = ''.join(huffman_dict[item] for item in data)

    return encoded_data, huffman_dict, freq


def huffman_decoding(encoded_data, huffman_dict):
    
    decoded_data = []
    bit_string  = ""
    for bit in encoded_data:
        bit_string  += bit
        for key, value in huffman_dict.items():
            if value == bit_string :
                decoded_data.append(tuple(map(int, key.strip('()').split(','))))
                bit_string  = ""
                break

    return decoded_data


def save_huffman_dict(yHuffman_dict, cbHuffman_dict, crHuffman_dict, out_dir):

    yHuffman_dict_to_save = {str(k): v for k, v in yHuffman_dict.items()}
    with open(out_dir+"yHuffman_dict.json", "w") as f:
        json.dump(yHuffman_dict_to_save, f)

    cbHuffman_dict_to_save = {str(k): v for k, v in cbHuffman_dict.items()}
    with open(out_dir+"cbHuffman_dict.json", "w") as f:
        json.dump(cbHuffman_dict_to_save, f)

    crHuffman_dict_to_save = {str(k): v for k, v in crHuffman_dict.items()}
    with open(out_dir+"crHuffman_dict.json", "w") as f:
        json.dump(crHuffman_dict_to_save, f)


def open_huffman_dict(output_dir):

    with open(output_dir+"yHuffman_dict.json", "r") as f:
        yHuffman_dict = json.load(f) 

    with open(output_dir+"cbHuffman_dict.json", "r") as f:
        cbHuffman_dict = json.load(f) 
    
    with open(output_dir+"crHuffman_dict.json", "r") as f:
        crHuffman_dict = json.load(f) 

    return yHuffman_dict, cbHuffman_dict, crHuffman_dict


def view_huffman_stats(yFreq, yHuffman_dict, yRle, cbFreq, cbHuffman_dict, cbRle, crFreq, crHuffman_dict, crRle):

    yFreq = sorted(yFreq.items(), key=lambda x: x[1], reverse=True)
    cbFreq = sorted(cbFreq.items(), key=lambda x: x[1], reverse=True)
    crFreq = sorted(crFreq.items(), key=lambda x: x[1], reverse=True)

    y_list_code = []
    for y_code in yHuffman_dict.values():
        y_list_code.append(y_code)

    cr_list_code = []
    for cr_code in cbHuffman_dict.values():
        cr_list_code.append(cr_code)

    cb_list_code = []
    for cb_code in crHuffman_dict.values():
        cb_list_code.append(cb_code)

    sumY = 0
    sumCr = 0
    sumCb = 0
    print("\nHuffman analysis:")
    print("--------------------------------------------------------------------------------------------------------------------------------------")
    print("\t     Luminance Y\t\t|\t\tChrominance Cr\t\t\t|\t\tChrominance Cb")
    print("--------------------------------------------------------------------------------------------------------------------------------------")
    print("Symbol","\t\tProba","\tCode","\tLength  |",
        "\tSymbol","\t\tProba","\tCode","\tLength  |",
        "\tSymbol","\t\tProba","\tCode","\tLength")
    print("--------------------------------------------------------------------------------------------------------------------------------------")
    for i in range(0,10):
        print(str(yFreq[i][0])+ "\t\t"+ str(np.round(yFreq[i][1],3))+ "\t"+ str(y_list_code[i]) +"\t"+ str(len(y_list_code[i])) + 
        "\t|\t" + str(crFreq[i][0])+ "\t\t"+ str(np.round(crFreq[i][1],3))+ "\t"+ str(cr_list_code[i]) + "\t"+ str(len(cr_list_code[i])) +
        "\t|\t" + str(cbFreq[i][0])+ "\t\t"+ str(np.round(cbFreq[i][1],3))+ "\t"+ str(cb_list_code[i]) + "\t"+ str(len(cr_list_code[i])))
        sumY += (yFreq[i][1])
        sumCr += (crFreq[i][1])
        sumCb += (cbFreq[i][1])
    print("--------------------------------------------------------------------------------------------------------------------------------------")
    print("Total\t\t{:.3f}\t\t\t|\tTotal\t\t{:.3f}\t\t\t|\tTotal\t\t{:.3f}".format(sumY, sumCr, sumCb))
    print("--------------------------------------------------------------------------------------------------------------------------------------")
    print("Entropy\t\t\t\t{:.1f}\t|\tEntropy\t\t\t\t{:.1f}\t|\tEntropy\t\t\t\t{:.1f}".format(entropy(yRle), entropy(crRle), entropy(cbRle)))
    print("--------------------------------------------------------------------------------------------------------------------------------------\n")
