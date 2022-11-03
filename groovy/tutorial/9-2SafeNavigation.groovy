String npe = null
assert null == npe?.toInteger()?.class?.name
assert null == null?.toInteger()?.class?.name
assert "java.lang.Integer" == "1"?.toInteger()?.class?.name


def a = "1"?.toInteger()?.class?.name ?: 'this is null'
assert a == 'java.lang.Integer'

def b = null?.toInteger()?.class?.name ?: 'this is null'
assert b == 'this is null'
