from utility import *

# ---------------------------- Data Dictionary parsing --------------------


def parse_data_dictionary(root_elem, schema_mode):
    data_dict = dict()
    function_dict = dict()

    for type_def in root_elem.findall('typeDefinitions'):
        data_values = list()

        for members in type_def.findall('members'):
            value = members.get('name') + ':::' + members.get('id')
            data_values.append(value)

        key = type_def.get('name') + ':::' + type_def.get('id')
        data_dict[key] = data_values

    for functions in root_elem.findall('functions'):
        function_name = None
        for func in functions.findall('function'):
            function_name = func.get('name') + ':::' + func.get('id')

        if function_name is not None:
            for funcValue in functions.iter('value'):
                for key, value in funcValue.attrib.items():
                    key = clean_str(key)
                    value = clean_str(value)

                    if key == 'type' and 'Const' in value:
                        function_dict[function_name] = funcValue.get('value')

    print_data_dictionary(data_dict, function_dict, schema_mode)


def print_data_dictionary(data_dict, function_dict, schema_mode):
    # print data_dict
    # print function_dict

    for data_name, elements in data_dict.items():
        data_name = split_name_id(data_name)
        if schema_mode == 1:
            sentence = uppercase_first_letter(data_name[0]) + ' is a data type. '
        elif schema_mode == 2:
            sentence = check_ace_predefined_words(data_name[0]) + ' is a n:datatype. '
        else:
            sentence = uppercase_first_letter(data_name[0]) + ' [' + data_name[1] + ']' + ' is a data type. '

        count = len(elements)
        if count == 1:
            element_name = split_name_id(elements[0])
            if schema_mode == 1:
                sentence += 'It has 1 element that is ' + uppercase_first_letter(element_name[0]) + '.'
            elif schema_mode == 2:
                sentence += 'It has 1 element that is ' + check_ace_predefined_words(element_name[0]) + '.'
            else:
                sentence += 'It has 1 element that is ' + uppercase_first_letter(element_name[0]) + \
                            ' [' + element_name[1] + ']' + '.'

        elif count > 1:
            sentence += 'It has ' + str(count) + ' elements that are '
            i = 0
            while i < count:
                element_name = split_name_id(elements[i])
                if schema_mode == 1:
                    word = uppercase_first_letter(element_name[0])
                    if i == count - 1:
                        sentence += 'and ' + word + '.'
                    else:
                        sentence += word + ', '
                elif schema_mode == 2:
                    word = check_ace_predefined_words(element_name[0])
                    if i == count - 1:
                        sentence += word + '.'
                    else:
                        sentence += word + ' and '
                else:
                    word = uppercase_first_letter(element_name[0])
                    if i == count - 1:
                        sentence += 'and ' + word + ' [' + element_name[1] + '].'
                    else:
                        sentence += word + ' [' + element_name[1] + '], '

                i += 1

        print sentence
        my_pdf_append_text(sentence)

    for func_name, func_value in function_dict.items():
        if func_value is None:
            continue

        func_name = split_name_id(func_name)
        sentence = ''
        if schema_mode == 1:
            sentence = uppercase_first_letter(func_name[0]) + ' is a constant. '
        elif schema_mode == 2:
            sentence = check_ace_predefined_words(func_name[0]) + ' is a constant. '
        else:
            sentence = uppercase_first_letter(func_name[0]) + ' [' + func_name[1] + '] is a constant. '

        sentence += 'It is equal to ' + uppercase_first_letter(func_value) + '.'

        print sentence
        my_pdf_append_text(sentence)
