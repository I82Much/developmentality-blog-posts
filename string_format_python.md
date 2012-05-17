2012-05-16

Python makes it easy to create and manipulate strings.  Let's examine a few various ways of doing so.  

# Implicit concatenation
If whitespace alone separates adjacent string literals, they will be concatenated together.

>>> 'hello' 'world'
'helloworld'

This can be useful if you have a long string that you want to break up

>>> a_long_string = ('hello this is a very very very very'
...                  'long string')
>>> print a_long_string
hello this is a very very very verylong string

# Explicit concatenation
You can also use the + operator to concatenate strings.

>>> 'hello' + 'world'
'helloworld'

Unlike in Java, types are not automatically coerced; it is an error to attempt to concatenate non-strings to a string:

>>> num_examples = 4
>>> 'I have ' + num_examples + ' examples to discuss.'
Traceback (most recent call last):
  File "<input>", line 1, in <module>
TypeError: cannot concatenate 'str' and 'int' objects

You must explicitly convert non-string types into strings before using this operator.

>>> 'I have ' + str(num_examples) + ' examples to discuss.'
'I have 4 examples to discuss.'

# String interpolation
Creating longer strings by concatenating together different substrings works, but it's not the most elegant solution.  It is a common mistake to forget to put a space before or after whatever is inserted in the middle of two other strings, wasting time on the programmer's part.  It is also somewhat hard to scan while reading the source code; the + signs can distract from what the string is trying to say. 

If you have used C before, you are probably familiar with `printf` and `sprintf`, which allow you to embed special characters within your strings which are subsituted with later arguments.  For instance,

    printf("hello %s\n", "world");

would produce "hello world".  Python has this feature built in to strings with the % operator.  You can read more in depth about the [String Formatting Operations][] and its syntax, but at the very least you should memorize the flags %d (for integer types), %f (for floating point), and %s (for strings).  For instance,

>>> 'I have %d things to talk about' %num_topics
'I have 4 things to talk about'

If you have more than one substitution to make, you must surround the substituted values in parentheses:

>>> 'I have %d things to talk about.  Number 1: %s' %(num_topics, 'Implicit concatenation')
'I have 4 things to talk about.  Number 1: Implicit concatenation'

This is a very powerful technique, especially when you learn the formatting flags that this operator supports.  For instance,

>>> 'It is %.2f degrees out' %(98.63483)  # display 2 decimal places
'It is 98.63 degrees out'

This technique does not work as well when there are many substitutions to make:

query = """SELECT %s
FROM %s
WHERE %s
GORUP BY %s
ORDER BY %s""" %(columns, table, where_clause, order_by_clause, group_by_clause)

Did you catch it?  It's easy to make a mistake like this in production.  If you have more than 2 or 3 substitutions, I recommend the following technique - string format.

# String format
Strings have a [format function][String format] which can also play the part of variable substiution.  The benefit of this approach is that each substitution is named, and it is impossible to provide the arguments in the wrong order.

	query = """SELECT {columns}
	FROM {table}
	WHERE {where_clause}
	GORUP BY {group_by_clause}
	ORDER BY {order_by_clause}""".format(columns = 'sum(num_users) AS actives',
									  	table = '1_day_actives',
									  	where_clause = 'country = "US"',
									  	order_by_clause = 'actives',
									  	group_by_clause = 'actives')

If you prefer, you can use a dictionary to power the variable replacement.

	data_dict = {
		'columns': 'sum(num_users) AS actives',
		'table': '1_day_actives',
		'where_clause': 'country = "US"',
		'order_by_clause': 'actives',
		'group_by_clause': 'actives'
	}
	query = """SELECT {columns}
	FROM {table}
	WHERE {where_clause}
	GORUP BY {group_by_clause}
	ORDER BY {order_by_clause}""".format(**data_dict)


Note the `format` method is only available in Python 2.6 and newer.  As the [documentation][String format] states,

> This method of string formatting is the new standard in Python 3, and should be preferred to the % formatting described in String Formatting Operations in new code.

Hopefully I have shown that this is easier to read and less error prone than the alternatives.


[String format]:http://docs.python.org/library/stdtypes.html#str.format