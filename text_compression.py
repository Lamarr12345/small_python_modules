"""
LZW-algorithm inpired implementation to encode a input text to a sequence of integers.
The sequence of integers is siginficantly shorter then the number of characters in the input text
if the text is sufficiently long and includes repetitve patterns (which most languages do).

The result is compression of the text.

The decode fuction allows the sequence of numbers to be converted back (lossless) into the original input text.

This is done by building encoding/decoding dictionaries which contain reepating patterns during said processes.

To get an actually compressed file using those functions, it is advised to convert the data into proper byte data (for example with numpy).
"""

BEYOND_VALID_CHR = 1114112       # This constant help to find the starting point for the extented dictionary so that its startoutside of the valid range for single characters

def encoding(text: str, print_details: bool = False):
    """Encodes an input text into a sequnce of unsigned integers.
    
    inputs:

    text(str):
    - takes input text in for of a string object

    print_details(bool)(optional):
    - if set to true, prints encoding details to the console

    output:

    list[int]:
    - list of integers containing the encoded sequence
    """
   
    encoding_dict: dict[str, int] = {}
    output_list = []

    # building of the single character base dictinary with all ouccuring characters
    for char in text:
        if not char in encoding_dict.keys():
            encoding_dict[char] = ord(char)

    # determining the start of the extended dictionary
    ext_dict_start_help = BEYOND_VALID_CHR - len(encoding_dict)

    # encoding of the text
    # i is the end of the current encoding window
    # j is the fron of the encoding window and constantly moves forward
    # i gets set forward once an encoding happened
    i = 0
    while i < len(text):
        j = i + 2
        while text[i:j] in encoding_dict and j <= len(text):
            j += 1
        else:
            output_list.append(encoding_dict.get(text[i:j-1]))
            if j <= len(text):
                encoding_dict[text[i:j]] = ext_dict_start_help + len(encoding_dict)
            i = j - 1

    # optinal text for compression details
    if print_details:
        total_char_count = len(text)
        compression_symbol_count = len(output_list)
        compression_ratio = total_char_count / compression_symbol_count
        compressed_memory = (compression_symbol_count / total_char_count) * 100
        print("-----------Compression details-----------")
        print(f"The total number of characters in input text was {total_char_count}.")
        print(f"The number of integer this was reduced to is {compression_symbol_count}.")
        print(f"This results in a compression ratio of '{compression_ratio:.2f}:1'.")
        print(f"{compressed_memory:.2f}% of original memory size.")
        print("Assuming that used data-types of characters and integers")
        print("take the same amount of space of in memory.")
        print("-----------------------------------------")

    return output_list


def decoding(encoded_msg: list[int]):
    """Decodes an encoded integer sequnce back into the original text (lossless).

    Input:

    encoded_msg(list[int]):
    - encoded message in for of a unsigned integer sequence.

    Output:
    - Returns the decoded text in form of a string object.
    """
    
    decoding_dict: dict[int, str] = {}
    output_text = ""

    # building of the single character base dictinary with all ouccuring characters
    for index_key in encoded_msg:
        if index_key < BEYOND_VALID_CHR and not index_key in decoding_dict.keys():
            decoding_dict[index_key] = chr(index_key)

    # determining the start of the extended dictionary
    ext_dict_start_help = BEYOND_VALID_CHR - len(decoding_dict)

    # decoding of the integer sequnce
    i = 0
    while i < len(encoded_msg):
        current_dict_entry = decoding_dict.get(encoded_msg[i])
        output_text = output_text + current_dict_entry

        if i + 1 < len(encoded_msg):
            next_dict_decoding = decoding_dict.get(encoded_msg[i+1])
            # determining appending character based on if the next dictionary already exists (needed in long repeating sequneces)
            if next_dict_decoding:
                decoding_dict[ext_dict_start_help + len(decoding_dict)] = current_dict_entry + next_dict_decoding[0]
            else:
                decoding_dict[ext_dict_start_help + len(decoding_dict)] = current_dict_entry + current_dict_entry[0]
        i += 1
    
    return output_text
