import json
import nanotest.core as nc

def source (obj, filename):
    try:
        src = open(filename, "r")
    except Exception as err:
        msg = "could not open: {}".format(err)
        obj.results.append({'run': False, 'msg': msg, 'file': test, 'tests': None})
        return
    try:
        injt = json.load(src)
    except Exception as err:
        msg = "could not unmarshal JSON: {}".format(err)
        obj.results.append({'run': False, 'msg': msg, 'file': test, 'tests': None})
        return
    if type(injt) != "dict":
        msg = "Injected test data should be dict; is {}".format(type(injt))
        obj.results.append({'run': False, 'msg': msg, 'file': test, 'tests': None})
        return
    obj.injt = injt

