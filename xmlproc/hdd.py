import xml.etree.cElementTree as ET
import sys, outputters
from xml_temp.parsers.xmlproc import xmlproc
from xml.dom import minidom

PASS = "PASS"
FAIL = "FAIL"
UNRESOLVED = "UNRESOLVED"

def ddmin(circumstances, test):

    n = 2
    while len(circumstances) >= 2:
        subsets = split(circumstances, n)
        assert len(subsets) == n

        some_complement_is_failing = 0
        for subset in subsets:

            complement = listminus(circumstances, subset)

            if test(complement) == FAIL:
                circumstances = complement
                n = max(n - 1, 2)
                break
        
        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))
    
    return circumstances

def hdd(root, test):
    for child in root:
        print ET.tostring(child, "us-ascii")
        if test(ET.tostring(child, "utf-8")) == FAIL: 
            print 'fail'


def prune(root, element):
    root.remove(element)
    return root

if __name__ == "__main__":
    tests = {}
    warnings = 1
    entstack = 0
    rawxml = 0
    
    if len(sys.argv) < 2:
        print 'Please input file'
        sys.exit()

    fname = open(sys.argv[1], 'r')
    #tree = ET.parse(sys.argv[1])
    tree = ET.fromstring(fname.read().decode('us-ascii'))
    print fname.read().decode('us-ascii')
    #tree = ET.XML(fname.read())
    fname.close()

    #xmldoc = minidom.parse(sys.argv[1])
    #itemlist = xmldoc.getElementsByTagName('folder')
    #booklist = itemlist.item(0).getElementsByTagName('bookmark')
    #print booklist[0].attributes

    app = xmlproc.Application()
    p = xmlproc.XMLProcessor()
    p.set_application(app)
    err = outputters.MyErrorHandler(p, p, warnings, entstack, rawxml)
    p.set_error_handler(err)
    p.set_data_after_wf_error(0)

    def writeTempfile(s):
        tempfile = open('temp.xml', 'w+')
        tempfile.truncate()
        tempfile.write(s)
        tempfile.flush()
        tempfile.close()
        return tempfile.name

    def getTempfiledata():
        tempfile = open('temp.xml', 'r')
        data = tempfile.read()
        tempfile.close()
        return data

    def mytest(c):
        global tests

        s = ""
        for char in c:
            s += char

        if s in tests.keys():
            return tests[s]

        try:
            p.parse_resource(writeTempfile(c))
            if err.errors == 0:
                print PASS
                tests[s] = PASS
                return PASS
            else:
                print UNRESOLVED
                tests[s] = UNRESOLVED
                return UNRESOLVED
        except UnboundLocalError:
            print FAIL
            tests[s] = FAIL
            return FAIL

    #tree.write('test.xml', "utf-8")
    #root = tree.getroot()
    hdd(tree, mytest)


