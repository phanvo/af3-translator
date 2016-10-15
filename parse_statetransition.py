from utility import *

# ---------------------------- State Transition parsing --------------------


def parse_state_transition(component_list, schema_mode):
    if len(component_list) == 0:
        return

    for component in component_list:
        state_list = list()
        init_state_list = list()

        is_found = False
        for spec in component.findall('specifications'):
            for key, value in spec.attrib.items():
                key = clean_str(key)
                value = clean_str(value)

                if key == 'type' and value == 'StateAutomaton':
                    search_all_states(spec, state_list, init_state_list)

                    is_found = True
                    break
            if is_found is True:
                break

        #for parent in component.findall(".//specifications[@id='" + state_automaton_id + "'].."):
        #    component_name = parent.get('name')
         #   print component_name

        if is_found is False:
            continue

        component_token = component.get('name') + ':::' + component.get('id')
        print_component_state_list_info(component_token, state_list, init_state_list, schema_mode)

        connector_dict = dict()
        transition_list = list()
        search_transition_list(component, state_list, connector_dict, transition_list)

        print_state_transition_list(transition_list, connector_dict, schema_mode)

        print '///////////////////// end of component /////////////////////'
        my_pdf_line_break(10)


def search_all_states(spec, state_list, init_state_list):
    for state in spec.findall('./containedElements/containedElements'):
        for key, value in state.attrib.items():
            key = clean_str(key)
            value = clean_str(value)

            if key == 'type' and value == 'State':
                # print state.get('name')
                state_list.append(state)

                if is_initial_state(state):
                    state_token = state.get('name') + ':::' + state.get('id')
                    init_state_list.append(state_token)


def is_initial_state(state):
    for spec in state.findall('specifications'):
        for key, value in spec.attrib.items():
            key = clean_str(key)
            value = clean_str(value)

            if key == 'initial' and value == 'true':
                # print 'INITIAL = ' + state.get('name')
                return True

    return False


def search_transition_list(component, state_list, connector_dict, transition_list):
    for state in state_list:
        for connector in state.findall('connectors'):
            connector_id = connector.get('id')
            connector_dict[connector_id] = state.get('name') + ':::' + state.get('id')

    for connection in component.iter('connections'):
        for key, value in connection.attrib.items():
            key = clean_str(key)
            value = clean_str(value)

            if key == 'type' and value == 'TransitionSegment':
                transition_list.append(connection)


def print_component_state_list_info(component_token, state_list, init_state_list, schema_mode):
    my_pdf_set_text_color('blue')
    count = len(state_list)
    token = split_name_id(component_token)
    component_name = token[0]
    if count == 1:
        if schema_mode == 1:
            sentence = 'The component ' + uppercase_first_letter(component_name) + ' has 1 state that is ' + \
                  uppercase_first_letter(state_list[0].get('name')) + '.'
        elif schema_mode == 2:
            sentence = 'The n:component-' + check_ace_predefined_words(component_name) + ' has 1 state that is ' + \
                  check_ace_predefined_words(state_list[0].get('name')) + '.'
        else:
            sentence = 'The component ' + uppercase_first_letter(component_name) + ' [' + token[1] + \
                       '] has 1 state that is ' + uppercase_first_letter(state_list[0].get('name')) + \
                       ' [' + state_list[0].get('id') + '].'

        print sentence
        my_pdf_append_text(sentence)
    elif count > 1:
        if schema_mode == 1:
            sentence = 'The component ' + uppercase_first_letter(component_name) + ' has ' + \
                       str(count) + ' states that are '
            i = 0
            while i < count:
                state_name = uppercase_first_letter(state_list[i].get('name'))
                if i == count - 1:
                    sentence += 'and ' + state_name + '.'
                else:
                    sentence += state_name + ', '
                i += 1
        elif schema_mode == 2:
            sentence = 'The n:component-' + check_ace_predefined_words(component_name) + ' has ' + \
                       str(count) + ' states that are '
            i = 0
            while i < count:
                state_name = check_ace_predefined_words(state_list[i].get('name'))
                if i == count - 1:
                    sentence += state_name + '.'
                else:
                    sentence += state_name + ' and '
                i += 1
        else:
            sentence = 'The component ' + uppercase_first_letter(component_name) + ' [' + token[1] + '] has ' + \
                       str(count) + ' states that are '
            i = 0
            while i < count:
                state_name = uppercase_first_letter(state_list[i].get('name'))
                state_id = state_list[i].get('id')
                if i == count - 1:
                    sentence += 'and ' + state_name + ' [' + state_id + '].'
                else:
                    sentence += state_name + ' [' + state_id + '], '
                i += 1

        print sentence
        my_pdf_append_text(sentence)

    my_pdf_set_text_color()

    count = len(init_state_list)
    if count == 1:
        state_token = split_name_id(init_state_list[0])
        if schema_mode == 1:
            sentence = 'The initial state of the component ' + uppercase_first_letter(component_name) + ' is ' + \
                  uppercase_first_letter(state_token[0]) + '.'
        elif schema_mode == 2:
            sentence = 'The initial state of the n:component-' + check_ace_predefined_words(component_name) + ' is ' + \
                  check_ace_predefined_words(state_token[0]) + '.'
        else:
            sentence = 'The initial state of the component ' + uppercase_first_letter(component_name) + \
                       ' [' + token[1] + '] is ' + uppercase_first_letter(state_token[0]) + ' [' + state_token[1] + '].'

        print sentence
        my_pdf_append_text(sentence)
    elif count > 1:
        if schema_mode == 1:
            sentence = 'The initial states of the component ' + uppercase_first_letter(component_name) + ' are '
            i = 0
            while i < count:
                state_token = split_name_id(init_state_list[i])
                word = uppercase_first_letter(state_token[0])
                if i == count - 1:
                    sentence += ' and ' + word + '.'
                else:
                    sentence += word + ', '
                i += 1
        elif schema_mode == 2:
            sentence = 'The initial states of the n:component-' + check_ace_predefined_words(component_name) + ' are '
            i = 0
            while i < count:
                state_token = split_name_id(init_state_list[i])
                word = uppercase_first_letter(state_token[0])
                if i == count - 1:
                    sentence += word + '.'
                else:
                    sentence += word + ' and '
                i += 1
        else:
            sentence = 'The initial states of the component ' + uppercase_first_letter(component_name) + \
                       ' [' + token[1] + '] are '
            i = 0
            while i < count:
                state_token = split_name_id(init_state_list[i])
                word = uppercase_first_letter(state_token[0])
                if i == count - 1:
                    sentence += ' and ' + word + ' [' + state_token[1] + '].'
                else:
                    sentence += word + ' [' + state_token[1] + '], '
                i += 1

        print sentence
        my_pdf_append_text(sentence)


def print_state_transition_list(transition_list, connector_dict, schema_mode):
    for transition in transition_list:
        name = transition.get('name')
        source_state = connector_dict.get(transition.get('source'))
        source_state_token = split_name_id(source_state)

        target_state = connector_dict.get(transition.get('target'))
        target_state_token = split_name_id(target_state)

        if schema_mode == 1:
            sentence = uppercase_first_letter(name) + ' is a transition from the state ' + \
                       uppercase_first_letter(source_state_token[0]) + \
                       ' to the state ' + uppercase_first_letter(target_state_token[0]) + '.'
        elif schema_mode == 2:
            sentence = check_ace_predefined_words(name) + ' is a transition from the n:state-' + \
                  check_ace_predefined_words(source_state_token[0]) + ' to the n:state-' + \
                  check_ace_predefined_words(target_state_token[0]) + '.'
        else:
            sentence = uppercase_first_letter(name) + ' [' + transition.get('id') + \
                       '] is a transition from the state ' + uppercase_first_letter(source_state_token[0]) + \
                       ' [' + source_state_token[1] + '] to the state ' + \
                       uppercase_first_letter(target_state_token[0]) + ' [' + target_state_token[1] + '].'

        print sentence
        my_pdf_append_text(sentence)

        print_guard_as_preconditions(transition, schema_mode)
        print_action_as_postconditions(transition, schema_mode)

        print '-------------------- end of transition -----------------'
        my_pdf_line_break()


def print_guard_as_preconditions(transition, schema_mode):
    precondition_list = list()
    for guard in transition.iter('guard'):
        for expression in guard.findall('expression'):
            search_function_argument(expression, precondition_list)

    if len(precondition_list) > 0:
        if schema_mode == 1:
            sentence = 'The Guard for ' + uppercase_first_letter(transition.get('name')) + \
                  ' is described by the following preconditions:'
        elif schema_mode == 2:
            sentence = 'The Guard for ' + check_ace_predefined_words(transition.get('name')) + \
                  ' is described by the following n:preconditions.'
        else:
            sentence = 'The Guard for ' + uppercase_first_letter(transition.get('name')) + \
                       ' [' + transition.get('id') + '] is described by the following preconditions:'

        print sentence
        my_pdf_append_text(sentence)
    else:
        return

    i = 0
    while i < len(precondition_list):
        element = precondition_list[i]
        if element.tag == 'arguments':
            identifier = element.get('identifier')
            try:
                pre_element = precondition_list[i - 1]
                operator = process_precondition_operator(pre_element)

                post_element = precondition_list[i + 1]
                value = process_precondition_value(post_element)
            except IndexError:
                operator = None
                value = None

            if identifier is not None and operator is not None and value is not None:
                if schema_mode == 1 or schema_mode == 3:
                    sentence = '     The value of ' + uppercase_first_letter(identifier) + ' is ' + \
                          operator + uppercase_first_letter(value) + '.'
                else:
                    sentence = '     The value of ' + check_ace_predefined_words(identifier) + ' is ' + \
                          operator + check_ace_predefined_words(value) + '.'
                print sentence
                my_pdf_append_text(sentence)
        i += 1


def search_function_argument(root, precondition_list):
    for node in root.findall('./'):
        if node.tag == 'arguments':
            search_function_argument(node, precondition_list)

        precondition_list.append(node)

        #sentence = a.tag

        #for key, value in a.attrib.items():
        #    key = clean_str(key)
        #    value = clean_str(value)

        #    sentence += ' ' + key + ':' + value

        #print sentence


        # the trick: find the "arguments", which has the attribute "identifier", to get its value
        # if found, look for the previous index, which has whatever tag name, to receive the attribute "operator"
        # then, look for the next index, which has whatever tag name, to receive the attribute "name" or "value"
        # ----> store all nodes in order, and search arguments having the attribute "identifier"

def process_precondition_value(element):
    result = None
    for key, value in element.attrib.items():
        key = clean_str(key)
        value = clean_str(value)

        if key == 'type' and 'Const' in value:
            result = element.get('value')
            if result is None:
                result = '0'

    if result is None:
        result = element.get('name')

    return result


def process_precondition_operator(element):
    predefined_list = ['equal', 'notequal', 'lowerthan', 'greaterthan', 'greaterequal', 'lowerequal']

    operator = element.get('operator')
    if operator is not None:
        try:
            index = predefined_list.index(operator.lower())

            if index == 0:
                return 'equal to '
            elif index == 1:
                return 'not equal to '
            elif index == 2:
                return 'lower than '
            elif index == 3:
                return 'greater than '
            elif index == 4:
                return 'greater than or equal to '
            elif index == 5:
                return 'lower than or equal to '
        except ValueError:
            return None
    return None


def print_action_as_postconditions(transition, schema_mode):
    postcondition_list = list()
    for action in transition.iter('actions'):
        for node in action.findall('.//'):
            postcondition_list.append(node)
            # print '[[[[[[[[[[[[[[[[[]]]]]]]]' + str(node.tag)

    if len(postcondition_list) > 0:
        if schema_mode == 1:
            sentence = 'The Action for ' + uppercase_first_letter(transition.get('name')) + \
                  ' is described by the following postconditions:'
        elif schema_mode == 2:
            sentence = 'The Action for ' + check_ace_predefined_words(transition.get('name')) + \
                  ' is described by the following n:postconditions.'
        else:
            sentence = 'The Action for ' + uppercase_first_letter(transition.get('name')) + \
                       ' [' + transition.get('id') + '] is described by the following postconditions:'

        print sentence
        my_pdf_append_text(sentence)
    else:
        return

    i = 0
    while i < len(postcondition_list):
        try:
            element = postcondition_list[i]
            if element.tag == 'variable':
                variable_name = element.get('identifier')
            elif element.tag == 'value':
                value_identifier = element.get('identifier')
                if value_identifier is None:
                    value_identifier = element.get('value')
                    if value_identifier is None:
                        value_identifier = process_postcondition_default_value(element)

                if value_identifier is None:
                    function = postcondition_list[i + 1]
                    function_name = function.get('name')

                    if function_name is None:
                        function_operator = function.get('operator')
                        if function_operator is None:
                            function_operator = 'Add'

                        argument1 = postcondition_list[i + 2]
                        argument1_identifier = argument1.get('identifier')
                        argument2 = postcondition_list[i + 3]
                        argument2_identifier = argument2.get('identifier')
                        if argument2_identifier is None:
                            argument2_identifier = argument2.get('value')

                        if schema_mode == 1 or schema_mode == 3:
                            sentence = '     The value of ' + uppercase_first_letter(variable_name) + ' is set to (' + \
                                       uppercase_first_letter(argument1_identifier) + ' ' + \
                                       process_postcondition_operator(function_operator) + ' ' + \
                                       uppercase_first_letter(argument2_identifier) + ').'
                        else:
                            sentence = '     The value of ' + check_ace_predefined_words(
                                variable_name) + ' is set to (' + \
                                       check_ace_predefined_words(argument1_identifier) + ' ' + \
                                       process_postcondition_operator(function_operator) + ' ' + \
                                       check_ace_predefined_words(argument2_identifier) + ').'
                        print sentence
                        my_pdf_append_text(sentence)
                    else:
                        if schema_mode == 1 or schema_mode == 3:
                            sentence = '     The value of ' + uppercase_first_letter(variable_name) + ' is set to ' + \
                                       uppercase_first_letter(function_name) + '.'
                        else:
                            sentence = '     The value of ' + check_ace_predefined_words(variable_name) + \
                                       ' is set to ' + check_ace_predefined_words(function_name) + '.'
                        print sentence
                        my_pdf_append_text(sentence)
                else:
                    if schema_mode == 1 or schema_mode == 3:
                        sentence = '     The value of ' + uppercase_first_letter(variable_name) + ' is set to ' + \
                                   uppercase_first_letter(value_identifier) + '.'
                    else:
                        sentence = '     The value of ' + check_ace_predefined_words(variable_name) + ' is set to ' + \
                                   check_ace_predefined_words(value_identifier) + '.'
                    print sentence
                    my_pdf_append_text(sentence)
        except (IndexError, TypeError):
            pass
        i += 1


def process_postcondition_default_value(element):
    for key, value in element.attrib.items():
        key = clean_str(key)
        value = clean_str(value)
        #print '...........' + key + ' ' + value

        if key == 'type':
            if 'bool' in value.lower():
                return 'False'
                # print '.....................................'
            elif 'int' in value.lower():
                return '0'
                # print '.....................................'
            elif 'double' in value.lower() or 'float' in value.lower():
                return '0.0'
    return None


def process_postcondition_operator(operator):
    predefined_list = ['subtract', 'add', 'multiply', 'divide']

    if operator is not None:
        try:
            index = predefined_list.index(operator.lower())

            if index == 0:
                return '-'
            elif index == 1:
                return '+'
            elif index == 2:
                return '*'
            elif index == 3:
                return '/'
        except ValueError:
            return None
    return 'Null'
