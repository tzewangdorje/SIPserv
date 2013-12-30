from collections import OrderedDict


class HeaderFieldValue(object):
    
    def __init__(self, value=None):
        self.value = ""
        self.params = OrderedDict()
        if value:
            params = value.split(";")
            start = True
            for param in params:
                start = self._processParam(param, start)
    
    def getParam(self, name):
        return self.params
    
    def __repr__(self):
        if self.params:
            return self.value+": "+str(self.params)
        else:
            return self.value
    
    def _processParam(self, param, start):
        if start:
            self.value = param.strip()
            start = False
        else:
            parts = param.split("=")
            key = parts[0].strip()
            if len(parts)==2:
                self.params[key] = parts[1].strip()
            else:
                self.params[key] = key
        return start


class HeaderField(object):
    
    def __init__(self, line=None):
        self.name = ""
        self.values = []
        if line:
            fieldName, fieldValue = line.split(':', 1)
            self.name = fieldName.strip()
            fieldValue = fieldValue.strip()
            values = fieldValue.split(",")
            for value in values:
                hfv = HeaderFieldValue(value)
                self.values.append(hfv)

    
    def __repr__(self):
        return "'"+self.name+"': "+str(self.values)
    
    def write(self):
        ret = self.name + ": "
        i = 1
        count = len(self.values)
        for value in self.values:
            ret = ret + value.value
            if len(value.params) > 0:
                for key, param in value.params.iteritems():
                    if key == param:
                        ret = ret + ";" + param
                    else:
                        ret = ret + ";" + key + "=" + param
            if i < count:
                ret = ret + ","
            i = i + 1
        return ret
    
    