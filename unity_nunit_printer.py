import sys
import xml.etree.ElementTree as ET
import textwrap
from pathlib import Path
from utils import get_int_attr, print_result, print_wrap

__version__ = "0.1.0"
_author_ = 'eamonwoortman'

"""unity_nunit_printer: a simple console application which parses and prints Unity3D NUnit result files."""
class NUnitPrinter():

    # parses the test-results element attributes
    def parse_headers(self, root):
        try:
            total_tests = get_int_attr(root, 'total')
            errors = get_int_attr(root, 'errors')
            failures = get_int_attr(root, 'failures')
            not_run = get_int_attr(root, 'not-run')
            inconclusive = get_int_attr(root, 'inconclusive')
            skipped = get_int_attr(root, 'skipped')
            invalid = get_int_attr(root, 'invalid')
        except KeyError as ke:
            print("Could not get the 'test-results' attribute:", ke)
            return
    
        successful = (total_tests - errors - failures - invalid - inconclusive)
        
        print_result('[Successful]', successful, '[Errors]', errors, '[Total]', total_tests)
        print_result('[Not run]', not_run, '[Inconclusive]', inconclusive, '[Skipped]', skipped)
        print_result('[Invalid]', invalid)
         
    def parse_test_cases(self, root):
        total_time = 0.0
        failed_cases = {}

        test_cases = root.findall('test-suite/results/test-case')
        for case in test_cases:
            total_time += float(case.get('time', 0.0))
            result = case.get('result')
            if result == 'Error':
                name = case.get('name')
                message = case.find('failure/message').text
                stack_trace = case.find('failure/stack-trace').text
                failed_cases[name] = (message, stack_trace)
        
        print_result('[Total time]', "%.2f seconds" % total_time)
        print("\n")

        for key, value in failed_cases.items():
            print('='*70)            
            print_result('Failed test: ', key)
            print('='*70)
            print_wrap('[Error] %s'%failed_cases[key][0].rstrip())
            print('')
            print_wrap('[Stack trace] %s'%failed_cases[key][1].rstrip())

    def try_parse_xml(self, xml_string):
        try: 
            root = ET.fromstring(xml_string)
        except Exception as ex:
            print("Could not parse unit_test_results.xml, error: ", ex)
            print(xml_string)
            return
    
        self.parse_headers(root)
        self.parse_test_cases(root)


def read_file():
    if len(sys.argv) == 1:
        return False

    path = sys.argv[1]
    if path == '':
        print("Please provide a valid file path")
        return False

    file = Path(path)
    if not file.is_file():
        print("Error: could not load file at '%s'" % path)
        return False
    return file.read_text('UTF-8')

def print_usage():
    print('Usage: ')
    print('unity_nunit_printer.py <path_to_nunit_result.xml>')

def main():
    print("Executing Unity NUnit result printer version %s.\n" % __version__)

    xml_string = read_file()
    if xml_string is False:
        print_usage()
        return

    parser = NUnitPrinter()
    parser.try_parse_xml(xml_string);

if __name__ == '__main__':
    main()