import nanotest

n = nanotest.Nanotester()

n.test("foobar",   ":re:bar",        "'foobar' contains 'bar'")
n.untest("foobar", ":re:^bar",       "'foobar' does not start with 'bar'")
n.test("foobar",   ":re:^foo",       "'foobar' starts with 'foo'")
n.test("foobar",   ":re:foo[abc]ar", "'foobar' matches 'foo[abc]ar'")
n.test("foobar",   ":re:^\S+$",      "'foobar' contains no spaces'")
n.untest("foobar", ":re:\s",         "'foobar' still contains no spaces'")
