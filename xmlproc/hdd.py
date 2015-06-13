import xml.etree.ElementTree as ET
import sys, outputters, re, time
from xml_temp.parsers.xmlproc import xmlproc
from split import split
from listsets import listminus

PASS = "PASS"
FAIL = "FAIL"
UNRESOLVED = "UNRESOLVED"

FAIL_TAG = "FailInHere"
FAIL_STRING = "&#x04A;"

TEMP_FILE = "temp.xml"


def ddmin(circumstances, test):
    """Return a sublist of CIRCUMSTANCES that is a relevant configuration
       with respect to TEST."""
    
    #assert test([]) == PASS
    #assert test(circumstances) == FAIL

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
                some_complement_is_failing = 1
                break

        if not some_complement_is_failing:
            if n == len(circumstances):
                break
            n = min(n * 2, len(circumstances))

    return circumstances


def hdd(root, test):
    nodes = []
    nodes.append(root)
    fail_nodes = []
    while len(nodes) > 0:
        temp = []
        for node in nodes:
            for child in node:
                if test(string_to_list(ET.tostring(child))) == FAIL: 
                    if len(child) > 0:
                        temp.append(child)
                    else:
                        fail_nodes.append(child)
        nodes = temp
    print len(fail_nodes)
    for node in fail_nodes:
        data = ET.tostring(node)
    
        #replace location of fail to correct fail string
        if FAIL_TAG in data:
            data = data.replace(FAIL_TAG, FAIL_STRING, 1)
        print data
        circumstances = string_to_list(data)
        test(ddmin(circumstances, test))

        showResult(TEMP_FILE)
    return fail_nodes

def prune(root, element):
    root.remove(element)
    return root

if __name__ == "__main__":
    circumstances = []
    tests = {}
    warnings = 1
    entstack = 0
    rawxml = 0

    testnum = 0

    if len(sys.argv) < 2:
        print 'Please input file'
        sys.exit()

    #fname = open(sys.argv[1], 'r')
    #print fname.read()
    tree = ET.parse(sys.argv[1])
    #tree = ET.fromstring(fname.read().decode('us-ascii'))
    #print fname.read().decode('us-ascii')
    #tree = ET.XML(fname.read())
    #fname.close()

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

    def getTempfiledata():
        tempfile = open('temp.xml', 'r')
        data = tempfile.read()
        tempfile.close()
        return data

    def string_to_list(s):
        c = []
        for i in range(len(s)):
            c.append((i, s[i]))
        return c

    def mytest(c):
        global testnum
        global circumstances

        s = ""
        for (index, char) in c:
            s += char

        #replace location of fail to correct fail string
        if FAIL_TAG in s:
            s = s.replace(FAIL_TAG, FAIL_STRING, 1)

        f = open(TEMP_FILE,'w')
        f.write(s)
        f.close()
        testnum += 1
        print "Test Num %d" % testnum

        if s in tests.keys():
            return tests[s]

        try:
            p.parse_resource(TEMP_FILE)
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

    def showResult(xmlfile):
        file = open(xmlfile)
        result = str(file.read())
        file.close
        print "************RESULT**OF**DELTA**DUBUGGING*************"
        print "%s" % (result)
        print "*****************************************************"


    start_time = time.time()

    root = tree.getroot()
    hdd(root, mytest)
    
    print("--- %s seconds ---" % (time.time() - start_time))

    
    #print "############"
    #testdata = "<title>Topic Guides &#x04A; python.org</title>"
    #file = open(sys.argv[1], 'r')
    #ttt = file.read()
    #file.close()

    #circumstances = string_to_list(testdata)
    #mytest(ddmin(circumstances, mytest))



