from huffman import huffman

def compress_file():
    file_path = raw_input("enter path")
    h =  huffman(file_path)
    output_path = h.compress_data()
    print output_path
    h.decompress_data(output_path)

if __name__  == "__main__":
    compress_file()
