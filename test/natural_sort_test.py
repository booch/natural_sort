import natural_sort
import unittest
import re


class ObjectType:
    def __init__(self, name, version):
        self.name = name
        self.version = version
    def __repr__(self):
        return '<%s, %s>' % (self.name, self.version)
    def v_version(self):
        return 'v%s' % self.version


class NaturalSortTestCase(unittest.TestCase):

    def setUp(self):
        self.strings_to_sort = [
            '1.3.2',
            '1.2.10',
            '2.1',
            '1.2.2',
            '2.1.0'
        ]
        self.dicts_to_sort = [
            {'name': 'def', 'version': '1.2.2'},
            {'name': 'abc', 'version': '1.3.2'},
            {'name': 'def', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.2.2'},
        ]
        self.object1 = ObjectType('def', '1.2.2')
        self.object2 = ObjectType('abc', '1.3.2')
        self.object3 = ObjectType('def', '1.2.10')
        self.object4 = ObjectType('abc', '1.2.10')
        self.object5 = ObjectType('abc', '1.2.2')
        self.objects_to_sort = [
            self.object1,
            self.object2,
            self.object3,
            self.object4,
            self.object5
        ]

    def tearDown(self):
        pass

    def test_sorting_list_of_strings(self):
        expected_result = [
            '1.2.2',
            '1.2.10',
            '1.3.2',
            '2.1',
            '2.1.0'
        ]
        assert(natural_sort.sort(self.strings_to_sort) == expected_result)

    def test_sorting_list_of_dicts(self):
        expected_result = [
            {'name': 'abc', 'version': '1.2.2'},
            {'name': 'abc', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.3.2'},
            {'name': 'def', 'version': '1.2.2'},
            {'name': 'def', 'version': '1.2.10'},
        ]
        assert(natural_sort.sort(self.dicts_to_sort, ('name', 'version')) == expected_result)

    def test_sorting_list_of_objects(self):
        expected_result = [
            self.object5,
            self.object4,
            self.object2,
            self.object1,
            self.object3
        ]
        assert(natural_sort.sort(self.objects_to_sort, ('name', 'version')) == expected_result)

    def test_sorting_with_descending_column(self):
        expected_result = [
            {'name': 'def', 'version': '1.2.2'},
            {'name': 'def', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.2.2'},
            {'name': 'abc', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.3.2'},
        ]
        assert(natural_sort.sort(self.dicts_to_sort, ('-name', 'version')) == expected_result)

    # NOTE: The order that the columns get sorted is undefined, but each column should be sorted naturally.
    def test_sorting_dicts_without_specifying_key_names(self):
        expected_result_when_sorting_by_name_then_version = [
            {'name': 'abc', 'version': '1.2.2'},
            {'name': 'abc', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.3.2'},
            {'name': 'def', 'version': '1.2.2'},
            {'name': 'def', 'version': '1.2.10'},
        ]
        expected_result_when_sorting_by_version_then_name = [
            {'name': 'abc', 'version': '1.2.2'},
            {'name': 'def', 'version': '1.2.2'},
            {'name': 'abc', 'version': '1.2.10'},
            {'name': 'def', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.3.2'},
        ]
        assert(natural_sort.sort(self.dicts_to_sort) == expected_result_when_sorting_by_version_then_name or natural_sort.sort(self.dicts_to_sort) == expected_result_when_sorting_by_name_then_version)

    # NOTE: The order that the columns get sorted is undefined, but each column should be sorted naturally.
    def test_sorting_objects_without_specifying_key_names(self):
        # Sorted by name, then version.
        expected_result_possibility_1 = [
            self.object5,
            self.object4,
            self.object2,
            self.object1,
            self.object3
        ]
        # Sorted by version, then name.
        expected_result_possibility_2 = [
            self.object5,
            self.object1,
            self.object4,
            self.object3,
            self.object2
        ]
        assert(natural_sort.sort(self.objects_to_sort) == expected_result_possibility_1 or natural_sort.sort(self.objects_to_sort) == expected_result_possibility_2)

    def test_sorting_objects_with_method_as_key(self):
        expected_result = [
            self.object5,
            self.object4,
            self.object2,
            self.object1,
            self.object3
        ]
        assert(natural_sort.sort(self.objects_to_sort, ('name', 'v_version')) == expected_result)

    def test_sorting_objects_with_property_as_key(self):
        expected_result = [
            self.object5,
            self.object4,
            self.object2,
            self.object1,
            self.object3
        ]
        assert(natural_sort.sort(self.objects_to_sort, ('name', 'v_version')) == expected_result)

    def test_common_dict_keys(self):
        dicts = [{'a': 1, 'b': 2, 'x': 3}, {'a': 1, 'b': 2, 'z': 3}]
        assert(natural_sort.common_keys(dicts) == ['a', 'b'])

    # I would not normally test a private function, but decided that the complexity demanded testing the smaller piece.
    # I would normally consider making it a public function, but it's not really related to natural sorting.
    def test_multikey_sorting_with_list_of_dicts(self):
        expected_result = [
            {'name': 'abc', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.2.2'},
            {'name': 'abc', 'version': '1.3.2'},
            {'name': 'def', 'version': '1.2.10'},
            {'name': 'def', 'version': '1.2.2'},
        ]
        assert(natural_sort._multi_key_sort(self.dicts_to_sort, ('name', 'version')) == expected_result)

    def test_multikey_sorting_with_list_of_dicts_and_normalizing_functions(self):
        expected_result = [
            {'name': 'abc', 'version': '1.2.2'},
            {'name': 'abc', 'version': '1.2.10'},
            {'name': 'abc', 'version': '1.3.2'},
            {'name': 'def', 'version': '1.2.2'},
            {'name': 'def', 'version': '1.2.10'},
        ]
        def convert(text):
            try:
                return int(text)
            except ValueError:
                return text
        functions = {
            'name': lambda x: x,
            'version': lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
        }
        result = natural_sort._multi_key_sort(self.dicts_to_sort, ('name', 'version'), functions)
        assert(result == expected_result)

if __name__ == '__main__':
    unittest.main()
