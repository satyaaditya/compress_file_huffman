import heapq
from collections import Counter
import os

class node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __cmp__(self,other):
        if other == None:
            return -1
        if not isinstance(other,node):
            return -1
        return self.freq > other.freq

class huffman:
    def __init__(self,path):
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}

    def make_frequency_dictionary(self,text):
        print Counter(text)
        return Counter(text)


    def make_heap(self,frequency_dictionary):
        for key in frequency_dictionary:
            new_node = node(key,frequency_dictionary[key])
            heapq.heappush(self.heap,new_node)


    def merge_nodes(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            mergednode = node(None,node1.freq + node2.freq)
            mergednode.left = node1
            mergednode.right = node2
            heapq.heappush(self.heap,mergednode)

    def make_codes_util(self,root_node,code):
        if  root_node == None:
            return
        if root_node.char != None:
            self.codes[root_node.char] = code
            self.reverse_codes[code] = root_node.char
            return

        self.make_codes_util(root_node.left, code +'0')
        self.make_codes_util(root_node.right, code + '1')

    def make_codes(self):
         root_node = heapq.heappop(self.heap)
         code = ""
         self. make_codes_util(root_node, code)

    def get_compressed_data(self,text):
        compressed_data = ""
        for i in text:
            compressed_data += self.codes[i]
        return compressed_data

    def add_padding(self,compressed_data):
        bits_to_be_added =  8 - len(compressed_data) % 8
        pad = bits_to_be_added * '0'
        compressed_data += pad
        padded_length = '{0:08b}'.format(bits_to_be_added)  #helpful while decompressing
        compressed_data = padded_length + compressed_data
        return compressed_data

    def get_byte_array(self,encoded_text):
        array = bytearray()
        if (len(encoded_text) % 8 != 0):
            print "encoding not happened properly"
        else:
            for i in xrange(0,len(encoded_text),8):
                byte = encoded_text[i:i + 8]
                byte = int(byte,2)
                array.append(byte)
            return array

    def compress_data(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        with open(self.path,'r+') as file,open(output_path,'w+') as file1:
            text = file.read()
            text = text.rstrip()
            frequency_dictionary = self.make_frequency_dictionary(text)
            self.make_heap(frequency_dictionary)
            self.merge_nodes()
            self.make_codes()

            compressed_data = self.get_compressed_data(text)
            padded_data = self.add_padding(compressed_data)
            byte_Array = self.get_byte_array(padded_data)

            file1.write(bytes(byte_Array))
        print "compressing done"
        return output_path

    def remove_padding(self,padded_text):
        padded_info = padded_text[:8]
        padded_length = int(padded_info,2)

        padded_text = padded_text[8:]
        encoded_text = padded_text[:-1 * padded_length]
        return encoded_text

    def get_decompressed_data(self,compressed_data):
        decompressed_text = "";current_code = ""
        for bit in compressed_data:
            current_code += bit
            if (current_code in self.reverse_codes):
                character = self.reverse_codes[current_code]
                decompressed_text += character
                current_code = ""
        return decompressed_text

    def decompress_data(self,path):
        filename, file_extension = os.path.splitext(path)
        output_path = filename + ".txt"
        with open(path,"rb") as file1,open(output_path,'w') as file2:
            byte = file1.read(1)
            bits_data = ""

            while (byte != ""):
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bits_data += bits
                byte = file1.read(1)
            encoded_text = self.remove_padding(bits_data)

            decompressed_text = self.get_decompressed_data(encoded_text)

            file2.write(decompressed_text)

        print("Decompressed")
        return output_path