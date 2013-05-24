'''
This module provides methods to sort lists naturally (i.e. x10 comes after x2).
This can be used to sort IP addresses, version numbers, variable-length alphanumeric product numbers, etc.
The lists to be sorted can contain strings, dictionaries, or objects.
For dictionaries and objects, the fields to sort on can be specified.

There's a good write-up on natural sorting at [http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html].


NOTES:
    - We considered an additional optional argument to sort() to pass in normalization functions,
      to allow sorting on values not contained directly in the list items. We decided against this.
      If you need to sort on a value not in the list items, you should (temporarily) add the values
      that you want to sort by to the list items. This is called a Schwartzian transform, or the 
      decorate-sort-undecorate idiom.
'''


import re


def sort(list_to_sort, keys_to_sort_on=None):
    '''
        Returns a list_to_sort containing the passed-in list_to_sort elements, sorted in natural order.
        Natural order puts alpha-numeric items in the correct order (eg. xyz-1.2.3 will sort before xyz-1.2.20).
        The list_to_sort may contain strings, dictionaries, or objects.
        If the list_to_sort contains dictionaries or objects, you may specify `keys_to_sort_on`.
        The `keys_to_sort_on` argument should contain a list_to_sort of names of index keys, methods, or attributes/properties to use as sort keys.
        Use '-key_name' to sort in descending order, instead of ascending.
        If you don't specify `keys_to_sort_on`, the order in which "columns" will be sorted is undefined, but each "column" will be sorted naturally.
        If the list_to_sort contains strings, the `keys_to_sort_on` is ignored.
        WARNING: We assume that the list_to_sort is homogeneous.
    '''
    if not list_to_sort:
        return list_to_sort
    if type(list_to_sort[0]) is str:
        return sort_strings(list_to_sort)
    if not keys_to_sort_on:
        keys_to_sort_on = common_keys(list_to_sort)
    return sort_dictionaries_or_objects(list_to_sort, keys_to_sort_on)


def sort_strings(list_of_strings):
    '''
        Returns a list containing the passed-in strings, sorted in natural order.
    '''
    return sorted(list_of_strings, key=naturally_sortable_chunks)


def sort_dictionaries(list_of_dicts, keys_to_sort_on):
    '''
        Returns a list containing the passed-in dictionaries, sorted in natural order by the specified key(s).
    '''
    return sort_dictionaries_or_objects(list_of_dicts, keys_to_sort_on)


def sort_objects(list_of_objects, keys_to_sort_on):
    '''
        Returns a list containing the passed-in objects, sorted in natural order by the specified key(s).
    '''
    return sort_dictionaries_or_objects(list_of_objects, keys_to_sort_on)


def sort_dictionaries_or_objects(list_to_sort, keys_to_sort_on):
    return _multi_key_sort(list_to_sort, keys_to_sort_on, normalization_functions_for_sorting_naturally(keys_to_sort_on))


# This is based on code from http://stackoverflow.com/a/10066661.
def common_keys(list_of_dicts_or_objects):
    '''
        Returns a list of keys that are common to all elements in the list.
        The list may contain dictionaries, in which case the keys returned will be the keys from the dictionaries.
        The list may contain objects, in which case the keys returned will be attribute/property names.
        WARNING: We assume that the list is homogeneous.
    '''
    if type(list_of_dicts_or_objects[0]) is not dict:
        list_of_dicts_or_objects = [obj.__dict__ for obj in list_of_dicts_or_objects]
    list_of_list_of_keys = [dict_element.keys() for dict_element in list_of_dicts_or_objects]
    result_set = set(list_of_list_of_keys[0])
    for s in list_of_list_of_keys[1:]:
        result_set &= set(s)
    return list(result_set)


def normalization_functions_for_sorting_naturally(keys):
    '''
        Returns a list of conversion/normalization functions, one for each key passed in.
        The conversion functions will convert strings into lists that can be compared in order to result in a natural sort.
    '''
    converters = {}
    for key in keys:
        if key[0] == '-':
            key = key[1:] # Remove leading minus sign for descending sort keys.
        converters[key] = naturally_sortable_chunks
    return converters


def naturally_sortable_chunks(key):
    '''
        Takes a string and breaks it into chunks that can be used for sorting, to result in a natural sort.
        Returns a list, each element containing either an integer, or a string of non-digits.
    ''' 
    converter = lambda text: int(text) if text.isdigit() else text.lower()
    return [ converter(c) for c in re.split('([0-9]+)', key) ] 


# Adapted from code at http://stygianvision.net/updates/python-sort-list-object-dictionary-multiple-key/.
# Our version automatically gets the values for the columns within the list to sort.
# WARNING: This is a general multi-key sort; it does not do natural sorting -- we use it to implement natural sorting of lists of dictionaries or objects.
def _multi_key_sort(list_to_sort, keys_to_sort_on, normalization_functions={}):
    '''
        Sort a list_to_sort of dictionaries or objects by multiple keys, with normalization functions.
        The `keys_to_sort_on` argument is a list_to_sort of key names to sort by.
        Use '-key_name' to sort in descending order, instead of ascending.
        The `normalization_functions` argument takes a dictionary of functions to normalize or process each value. 
        Each key in the `normalization_functions` dictionary should be the name of a key from `keys_to_sort_on`.
    '''
    comparers = []
    for col in keys_to_sort_on:
        if col.startswith('-'):
            column = col[1:]
            polarity = -1
        else:
            column = col
            polarity = 1
        if not column in normalization_functions:
            normalization_functions[column] = lambda x: x
        comparers.append((column, normalization_functions[column], polarity))

    def comparer(left, right):
        for column_name, func, polarity in comparers:
            left_value = get_value_from_dictionary_or_object(left, column_name)
            right_value = get_value_from_dictionary_or_object(right, column_name)
            result = cmp(func(left_value), func(right_value))
            if result:
                return polarity * result
        else:
            return 0
    return sorted(list_to_sort, cmp=comparer)


def get_value_from_dictionary_or_object(dict_or_object, column_name):
    '''
        Gets the item named by column_name from the dictionary or object. 
        Tries 3 things, in order: index/key, method call, attribute/property.
    '''
    try: 
        return dict_or_object[column_name]
    except (TypeError, AttributeError):
        try:
            return getattr(dict_or_object, column_name)()
        except TypeError:
            return getattr(dict_or_object, column_name)
