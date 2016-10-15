from utility import *
from collections import defaultdict

# ---------------------------- Component Architecture parsing --------------------


def parse_component_architecture(root_elem, schema_mode):
    component_list = list()

    for element in root_elem.iter('containedElements'):
        for key, value in element.attrib.items():
            key = clean_str(key)
            value = clean_str(value)

            if key == 'type' and value == 'Component':
                #print element.get('name')
                component_list.append(element)

    subcomponents_dict = search_all_subcomponents(root_elem, component_list)

    if len(component_list) > 0:
        parse_system_component(component_list[0], subcomponents_dict, schema_mode)
        del subcomponents_dict[component_list[0]]
        parse_all_subcomponent(subcomponents_dict, schema_mode)

    return component_list


def parse_system_component(system_component, subcomponents_dict, schema_mode):
    try:
        my_pdf_set_text_color('blue')
        system_subcomponents = subcomponents_dict[system_component]
        if len(system_subcomponents) == 1:
            if schema_mode == 1:
                sentence = 'The system ' + uppercase_first_letter(system_component.get('name')) + \
                      ' consists of 1 component that is ' + \
                      uppercase_first_letter(system_subcomponents[0].get('name')) + '.'
            elif schema_mode == 2:
                sentence = 'The n:system-' + check_ace_predefined_words(system_component.get('name')) + \
                      ' consists-of 1 component that is ' + \
                      check_ace_predefined_words(system_subcomponents[0].get('name')) + '.'
            else:
                system_id = ' [' + system_component.get('id') + ']'
                subcomponent_id = ' [' + system_subcomponents[0].get('id') + ']'
                sentence = 'The system ' + uppercase_first_letter(system_component.get('name')) + \
                           system_id + ' consists of 1 component that is ' + \
                           uppercase_first_letter(system_subcomponents[0].get('name')) + subcomponent_id + '.'

            print sentence
            my_pdf_append_text(sentence)
        elif len(system_subcomponents) > 1:
            if schema_mode == 1:
                sentence = 'The system ' + uppercase_first_letter(system_component.get('name')) + \
                           ' consists of ' + str(len(system_subcomponents)) + ' components that are '
                for i in range(len(system_subcomponents)):
                    token = uppercase_first_letter(system_subcomponents[i].get('name'))
                    if i == len(system_subcomponents) - 1:
                        sentence += 'and ' + token + '.'
                    else:
                        sentence += token + ', '
            elif schema_mode == 2:
                sentence = 'The n:system-' + check_ace_predefined_words(system_component.get('name')) + \
                           ' consists-of ' + str(len(system_subcomponents)) + ' components that are '
                for i in range(len(system_subcomponents)):
                    token = check_ace_predefined_words(system_subcomponents[i].get('name'))
                    if i == len(system_subcomponents) - 1:
                        sentence += token + '.'
                    else:
                        sentence += token + ' and '
            else:
                system_id = ' [' + system_component.get('id') + ']'
                sentence = 'The system ' + uppercase_first_letter(system_component.get('name')) + system_id + \
                           ' consists of ' + str(len(system_subcomponents)) + ' components that are '
                for i in range(len(system_subcomponents)):
                    token = uppercase_first_letter(system_subcomponents[i].get('name'))
                    token_id = ' [' + system_subcomponents[i].get('id') + ']'
                    if i == len(system_subcomponents) - 1:
                        sentence += 'and ' + token + token_id + '.'
                    else:
                        sentence += token + token_id + ', '

            print sentence
            my_pdf_append_text(sentence)

        my_pdf_set_text_color()

        channel_dict = search_channels_for_component(system_component)
        print_channels_in_component(system_component, channel_dict, schema_mode)
    except (RuntimeError, TypeError, NameError, KeyError):
        pass


def parse_all_subcomponent(subcomponents_dict, schema_mode):
    for component, v in subcomponents_dict.items():
        # if component.get('name').lower() != system_component.get('name').lower():
        if component.get('name') is None:
            continue
        my_pdf_line_break(10)
        try:
            print '////////////'
            my_pdf_set_text_color('blue')
            if len(v) == 1:
                if schema_mode == 1:
                    sentence = 'The component ' + uppercase_first_letter(component.get('name')) + \
                          ' has 1 subcomponent that is ' + uppercase_first_letter(v[0].get('name')) + '.'
                elif schema_mode == 2:
                    sentence = 'The n:component-' + check_ace_predefined_words(component.get('name')) + \
                          ' has 1 n:subcomponent that is ' + check_ace_predefined_words(v[0].get('name')) + '.'
                else:
                    component_id = ' [' + component.get('id') + ']'
                    subcomponent_id = ' [' + v[0].get('id') + ']'
                    sentence = 'The component ' + uppercase_first_letter(component.get('name')) + component_id + \
                               ' has 1 subcomponent that is ' + uppercase_first_letter(v[0].get('name')) + \
                               subcomponent_id + '.'
                print sentence
                my_pdf_append_text(sentence)
            elif len(v) > 1:
                if schema_mode == 1:
                    sentence = 'The component ' + uppercase_first_letter(component.get('name')) + \
                               ' has ' + str(len(v)) + ' subcomponents that are '
                    for i in range(len(v)):
                        token = uppercase_first_letter(v[i].get('name'))
                        if i == len(v) - 1:
                            sentence += 'and ' + token + '.'
                        else:
                            sentence += token + ', '
                elif schema_mode == 2:
                    sentence = 'The n:component-' + check_ace_predefined_words(component.get('name')) + \
                               ' has ' + str(len(v)) + ' n:subcomponents that are '
                    for i in range(len(v)):
                        token = check_ace_predefined_words(v[i].get('name'))
                        if i == len(v) - 1:
                            sentence += token + '.'
                        else:
                            sentence += token + ' and '
                else:
                    component_id = ' [' + component.get('id') + ']'
                    sentence = 'The component ' + uppercase_first_letter(component.get('name')) + component_id + \
                               ' has ' + str(len(v)) + ' subcomponents that are '
                    for i in range(len(v)):
                        token_id = ' [' + v[i].get('id') + ']'
                        token = uppercase_first_letter(v[i].get('name'))
                        if i == len(v) - 1:
                            sentence += 'and ' + token + token_id + '.'
                        else:
                            sentence += token + token_id + ', '

                print sentence
                my_pdf_append_text(sentence)

            my_pdf_set_text_color()

            channel_dict = search_channels_for_component(component)
            print_channels_in_component(component, channel_dict, schema_mode)
        except (RuntimeError, TypeError, NameError, KeyError):
            pass


def search_all_subcomponents(root, component_list):
    i = 1
    tmp_list = list()
    while i < len(component_list):
        element = component_list[i]

        # store all components found ---> find component's parent based on id

        for parent in root.findall(".//containedElements[@id='" + element.get('id') + "'].."):
            #tmp_dict.append((parent.get('name'), element.get('name')))
            tmp_list.append((parent, element))
        i += 1

    #print tmp_dict

    d = defaultdict(list)
    for k, v in tmp_list:
        d[k].append(v)

    #for k, v in d.items():
    #    print k, v

    return d


def search_channels_for_component(component):
    channel_list = list()
    for connection in component.findall('connections'):
        for key, value in connection.attrib.items():
            key = clean_str(key)
            value = clean_str(value)

            if key == 'type' and value == 'Channel':
                channel_list.append(connection)

    tmp_list = list()

    for channel in channel_list:
        #print channel.get('name'), '-------------------------'
        channel_name = channel.get('name') + ':::' + channel.get('id')

        source_target = ''
        for parent_component in component.findall(".//*[@id='" + channel.get('source') + "'].."):
            #print parent_component.get('name')
            source_name = parent_component.get('name') + ':::' + parent_component.get('id')
            source_target += source_name + '+++'

        for parent_component in component.findall(".//*[@id='" + channel.get('target') + "'].."):
            #print parent_component.get('name')
            target_name = parent_component.get('name') + ':::' + parent_component.get('id')
            source_target += target_name

        tmp_list.append((source_target, channel_name))

    d = defaultdict(list)
    for k, v in tmp_list:
        d[k].append(v)

    print '++++++++++'

    key_list = list()
    value_list = list()
    for k, v in d.items():
        key_list.append(k)
        value_list.append(v)

    i = 0
    while i < len(value_list) - 1:
        j = i + 1
        while j < len(value_list):
            #print value_list[i], value_list[j]
            if value_list[i] == value_list[j]:
                #print i, j
                check1 = key_list[i].split('+++')
                check2 = key_list[j].split('+++')

                if check1[0] == check2[0]:
                    new_key = None
                    if check1[1] == (component.get('name') + ':::' + component.get('id')):
                        new_key = str(key_list[j]) + '+++' + check1[1]
                        # print new_key

                    elif check2[1] == (component.get('name') + ':::' + component.get('id')):
                        new_key = str(key_list[i]) + '+++' + check2[1]
                        # print new_key

                    if new_key is not None:
                        d[new_key] = (value_list[i])
                        del d[key_list[i]]
                        del d[key_list[j]]
                        break
            j += 1
        i += 1

    for k, v in d.items():
        print k, v

    return d


def print_channels_in_component(component, channel_dict, schema_mode):
    component_name = component.get('name')
    component_token = component_name + ':::' + component.get('id')
    if len(channel_dict) > 0:
        if schema_mode == 1:
            sentence = 'The channels in ' + uppercase_first_letter(component_name) + \
                       ' are described by the following list:'
        elif schema_mode == 2:
            sentence = 'The channels in ' + check_ace_predefined_words(component_name) + \
                       ' are described by the following list.'
        else:
            sentence = 'The channels in ' + uppercase_first_letter(component_name) + \
                       ' [' + component.get('id') + '] are described by the following list:'
        print sentence
        my_pdf_append_text(sentence)
    else:
        return

    for k, channels in channel_dict.items():
        if isinstance(k, basestring):
            source_target = k.split('+++')  # index 0 -> source; index 1 -> target
            source_element = split_name_id(source_target[0])    # index 0 -> name; index 1 -> id
            target_element = split_name_id(source_target[1])    # index 0 -> name; index 1 -> id
        else:
            continue

        if isinstance(component_name, basestring) and len(source_target) > 1 and len(channels) > 0:
            if source_target[0].lower() == component_token.lower():
                if len(channels) == 1:
                    channel_token = split_name_id(channels[0])
                    if schema_mode == 1:
                        sentence = '     The channel ' + uppercase_first_letter(channel_token[0]) + \
                                   ' is an external input that goes to the component ' + \
                                   uppercase_first_letter(target_element[0]) + '.'
                    elif schema_mode == 2:
                        sentence = '     The n:channel-' + check_ace_predefined_words(channel_token[0]) + \
                              ' is an external input that goes to the n:component-' + \
                              check_ace_predefined_words(target_element[0]) + '.'
                    else:
                        token_id = ' [' + channel_token[1] + ']'
                        sentence = '     The channel ' + uppercase_first_letter(channel_token[0]) + token_id + \
                                   ' is an external input that goes to the component ' + \
                                   uppercase_first_letter(target_element[0]) + ' [' + target_element[1] + '].'
                    print sentence
                    my_pdf_append_text(sentence)
                elif len(channels) > 1:
                    if schema_mode == 1:
                        sentence = '     The channel '

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            # token = uppercase_first_letter(channels[i])
                            token = uppercase_first_letter(channel_token[0])
                            if i == len(channels) - 1:
                                sentence += 'and ' + token
                            else:
                                sentence += token + ', '

                        sentence += ' are external inputs that go to the component ' + \
                                    uppercase_first_letter(target_element[0]) + '.'
                    elif schema_mode == 2:
                        sentence = '     The n:channel-'

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            # token = check_ace_predefined_words(channels[i])
                            token = check_ace_predefined_words(channel_token[0])
                            if i == len(channels) - 1:
                                sentence += token
                            else:
                                sentence += token + ' and '

                        sentence += ' are the external n:inputs that go to the n:component-' + \
                                    check_ace_predefined_words(target_element[0]) + '.'
                    else:
                        sentence = '     The channel '

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            # token = uppercase_first_letter(channels[i])
                            token = uppercase_first_letter(channel_token[0]) + ' [' + channel_token[1] + ']'
                            if i == len(channels) - 1:
                                sentence += 'and ' + token
                            else:
                                sentence += token + ', '

                        sentence += ' are external inputs that go to the component ' + \
                                    uppercase_first_letter(target_element[0]) + ' [' + target_element[1] + '].'
                    print sentence
                    my_pdf_append_text(sentence)
            elif source_target[1].lower() == component_token.lower():
                if len(channels) == 1:
                    channel_token = split_name_id(channels[0])
                    if schema_mode == 1:
                        sentence = '     The channel ' + uppercase_first_letter(channel_token[0]) + \
                              ' is an output of the component ' + uppercase_first_letter(source_element[0]) + \
                              ' and also serves as an external output.'
                    elif schema_mode == 2:
                        sentence = '     The n:channel-' + check_ace_predefined_words(channel_token[0]) + \
                              ' is an n:output of the n:component-' + check_ace_predefined_words(source_element[0]) + \
                              ' and serves as the external n:output.'
                    else:
                        token_id = ' [' + channel_token[1] + ']'
                        sentence = '     The channel ' + uppercase_first_letter(channel_token[0]) + token_id + \
                                   ' is an output of the component ' + uppercase_first_letter(source_element[0]) + \
                                   ' [' + source_element[1] + '] and also serves as an external output.'
                    print sentence
                    my_pdf_append_text(sentence)
                elif len(channels) > 1:
                    if schema_mode == 1:
                        sentence = '     The channel '

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            token = uppercase_first_letter(channel_token[0])
                            if i == len(channels) - 1:
                                sentence += 'and ' + token
                            else:
                                sentence += token + ', '

                        sentence += ' are outputs of the component ' + uppercase_first_letter(source_element[0]) + \
                                    ' and also serve as external outputs.'
                    elif schema_mode == 2:
                        sentence = '     The n:channel-'

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            token = check_ace_predefined_words(channel_token[0])
                            if i == len(channels) - 1:
                                sentence += token
                            else:
                                sentence += token + ' and '

                        sentence += ' are the n:outputs of the n:component-' + \
                                    check_ace_predefined_words(source_element[0]) + \
                                    ' and serve as the external n:outputs.'
                    else:
                        sentence = '     The channel '

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            token = uppercase_first_letter(channel_token[0]) + ' [' + channel_token[1] + ']'
                            if i == len(channels) - 1:
                                sentence += 'and ' + token
                            else:
                                sentence += token + ', '

                        sentence += ' are outputs of the component ' + uppercase_first_letter(source_element[0]) + \
                                    ' [' + source_element[1] + '] and also serve as external outputs.'
                    print sentence
                    my_pdf_append_text(sentence)
            else:
                if len(channels) == 1:
                    channel_token = split_name_id(channels[0])
                    if schema_mode == 1:
                        sentence = '     The channel ' + uppercase_first_letter(channel_token[0]) + \
                                   ' is an output of the component ' + uppercase_first_letter(source_element[0]) + \
                                   '. It goes to the component ' + uppercase_first_letter(target_element[0])

                        if len(source_target) == 3:
                            sentence += ' and also serves as an external output.'
                        else:
                            sentence += '.'
                    elif schema_mode == 2:
                        sentence = '     The n:channel-' + check_ace_predefined_words(channel_token[0]) + \
                                   ' is an n:output of the n:component-' + check_ace_predefined_words(source_element[0])\
                                   + '. It goes to the n:component-' + check_ace_predefined_words(target_element[0])

                        if len(source_target) == 3:
                            sentence += ' and serves as the external n:output.'
                        else:
                            sentence += '.'
                    else:
                        token_id = ' [' + channel_token[1] + ']'
                        sentence = '     The channel ' + uppercase_first_letter(channel_token[0]) + token_id + \
                                   ' is an output of the component ' + uppercase_first_letter(source_element[0]) + \
                                   ' [' + source_element[1] + ']. It goes to the component ' + \
                                   uppercase_first_letter(target_element[0]) + ' [' + target_element[1] + ']'

                        if len(source_target) == 3:
                            sentence += ' and also serves as an external output.'
                        else:
                            sentence += '.'
                    print sentence
                    my_pdf_append_text(sentence)
                elif len(channels) > 1:
                    if schema_mode == 1:
                        sentence = '     The channel '

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            token = uppercase_first_letter(channel_token[0])
                            if i == len(channels) - 1:
                                sentence += 'and ' + token
                            else:
                                sentence += token + ', '

                        sentence += ' are outputs of the component ' + uppercase_first_letter(source_element[0]) + \
                                    '. They go to the component ' + uppercase_first_letter(target_element[0])

                        if len(source_target) == 3:
                            sentence += ' and also serve as external outputs.'
                        else:
                            sentence += '.'
                    elif schema_mode == 2:
                        sentence = '     The n:channel-'

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            token = check_ace_predefined_words(channel_token[0])
                            if i == len(channels) - 1:
                                sentence += token
                            else:
                                sentence += token + ' and '

                        sentence += ' are the n:outputs of the n:component-' + \
                                    check_ace_predefined_words(source_element[0]) + \
                                    '. They go to the n:component-' + check_ace_predefined_words(target_element[0])

                        if len(source_target) == 3:
                            sentence += ' and serve as the external n:outputs.'
                        else:
                            sentence += '.'
                    else:
                        sentence = '     The channel '

                        for i in range(len(channels)):
                            channel_token = split_name_id(channels[i])
                            token = uppercase_first_letter(channel_token[0]) + ' [' + channel_token[1] + ']'
                            if i == len(channels) - 1:
                                sentence += 'and ' + token
                            else:
                                sentence += token + ', '

                        sentence += ' are outputs of the component ' + uppercase_first_letter(source_element[0]) + \
                                    ' [' + source_element[1] + ']. They go to the component ' + \
                                    uppercase_first_letter(target_element[0]) + ' [' + target_element[1] + ']'

                        if len(source_target) == 3:
                            sentence += ' and also serve as external outputs.'
                        else:
                            sentence += '.'

                    print sentence
                    my_pdf_append_text(sentence)
