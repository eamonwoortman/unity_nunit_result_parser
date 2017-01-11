import sys
import xml.etree.ElementTree as ET
from utils import get_int_attr

"""unity_nunit_parser: a simple console application which parses Unity3D NUnit result files 
   and prints them."""

__version__ = "0.1.0"
_author_ = 'eamonwoortman'

class NUnitParser():

    def print_result(self, *args):
        res = ''
        for i in range(0, len(args)):
            if i % 2:
                res += '{:<10} '
            else:
                res += '{:<14} '
        print(res.format(*args))


    # parses the root(test-results) element attributes
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
        
        self.print_result('[Successful]', successful, '[Errors]', errors, '[Total]', total_tests)
        self.print_result('[Not run]', not_run, '[Inconclusive]', inconclusive, '[Skipped]', skipped)
        self.print_result('[Invalid]', invalid)
        print("")
         
    def parse_test_cases(self, root):
        total_time = 0.0
        failed_cases = ''

        for case in root.findall('test-case'):
            total_time += case.get('time', 0.0)
            result = case.get('result')
            if result is 'Error':
                name = case.get('name')

                failed_cases += ''


    def try_parse_xml(self):
        try: 
            tree = ET.parse('test_files/unit_test_results.xml')
            root = tree.getroot()
        except Exception as ex:
            print("Could not parse unit_test_results.xml, error: ", ex)
            return
    
        self.parse_headers(root)
        

def main():
    print("Executing Unity NUnit result parser version %s." % __version__)
    print("List of argument strings: %s" % sys.argv[1:])
    print("")

    parser = NUnitParser()
    parser.try_parse_xml();

if __name__ == '__main__':
    main()