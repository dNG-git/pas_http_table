# -*- coding: utf-8 -*-
##j## BOF

"""
direct PAS
Python Application Services
----------------------------------------------------------------------------
(C) direct Netware Group - All rights reserved
https://www.direct-netware.de/redirect?pas;http;table

This Source Code Form is subject to the terms of the Mozilla Public License,
v. 2.0. If a copy of the MPL was not distributed with this file, You can
obtain one at http://mozilla.org/MPL/2.0/.
----------------------------------------------------------------------------
https://www.direct-netware.de/redirect?licenses;mpl2
----------------------------------------------------------------------------
#echo(pasHttpTableVersion)#
#echo(__FILEPATH__)#
"""

from dNG.pas.data.supports_mixin import SupportsMixin
from dNG.pas.runtime.iterator import Iterator
from dNG.pas.runtime.not_implemented_exception import NotImplementedException
from dNG.pas.runtime.type_exception import TypeException
from dNG.pas.runtime.value_exception import ValueException

class Abstract(Iterator, SupportsMixin):
#
	"""
"Abstract" defines all methods used to define a table, its columns and rows.
It is used as an iterator to read rows.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: table
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	COLUMN_RENDERER_CALLBACK = 3
	"""
Uses a defined callback to encode the specified column data
	"""
	COLUMN_RENDERER_OSET = 1
	"""
Uses "template_name" to render the OSet with the specified column data
	"""
	COLUMN_RENDERER_SAFE_CONTENT = 2
	"""
Encodes the specified column data to be shown as XHTML content
	"""
	SORT_ASCENDING = "+"
	"""
Ascending sort direction
	"""
	SORT_DESCENDING = "-"
	"""
Descending sort direction
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Abstract)

:since: v0.1.00
		"""

		SupportsMixin.__init__(self)

		self.column_definitions = { }
		"""
Column definitions
		"""
		self.columns = [ ]
		"""
List of columns
		"""
		self.default_sort_definition = None
		"""
Default sort definition to be used
		"""
		self.hide_column_titles = False
		"""
True to hide column titles
		"""
		self.limit = -1
		"""
Limit of rows requested
		"""
		self.offset = 0
		"""
Row offset requested
		"""
		self.percent_remaining = 100
		"""
Percent remaining for additional columns
		"""
		self.sort_context = None
		"""
Sort context to be used
		"""
		self.sort_list = [ ]
		"""
Sort list to be applied
		"""
	#

	def __next__(self):
	#
		"""
python.org: Return the next item from the container.

:return: (object) Result object
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def add_column(self, key, title, size, sort_key = None, renderer = None):
	#
		"""
Add a column with the given properties.

:param key: Key used internally to identify this column
:param title: Title
:param size: Size in percent
:param renderer: Renderer definition

:since: v0.1.00
		"""

		if (size > self.percent_remaining): raise ValueException("Given size exceeds remaining one")
		self.percent_remaining -= size

		if (key not in self.column_definitions): self.columns.append(key)

		if (renderer is None): renderer = { "type": Abstract.COLUMN_RENDERER_SAFE_CONTENT }
		if (sort_key is None): sort_key = key

		self.column_definitions[key] = { "key": key,
		                                 "title": title,
		                                 "size": size,
		                                 "sort_key": sort_key,
		                                 "sortable": self.is_supported("sorting"),
		                                 "renderer": renderer
		                               }
	#

	def add_sort_definition(self, key, direction):
	#
		"""
Adds a sort definition.

:param key: Row key to sort
:param direction: Sort direction

:since: v0.1.02
		"""

		if (key not in self.column_definitions): raise ValueException("Given row key is not specified")
		if (direction not in ( Abstract.SORT_ASCENDING, Abstract.SORT_DESCENDING )): raise TypeException("Sort direction given is invalid")

		self.sort_list.append({ "key": self.column_definitions[key]['sort_key'],
		                        "direction": direction
		                      })
	#

	def disable_sort(self, *args):
	#
		"""
Disables sorting for the specified rows.

:since: v0.1.00
		"""

		for key in args:
		#
			if (key not in self.column_definitions): raise ValueException("Given row key is not specified")
			self.column_definitions[key]['sortable'] = False
		#
	#

	def get_column_definitions(self):
	#
		"""
Returns a dict of all column definitions.

:return: (dict) Column definitions
:since:  v0.1.00
		"""

		return self.column_definitions
	#

	def get_columns(self):
	#
		"""
Returns a list of all column keys.

:return: (list) Column keys
:since:  v0.1.00
		"""

		return self.columns
	#

	def get_limit(self):
	#
		"""
Returns the limit of rows requested.

:return: (int) Maximum number of rows requested; -1 for unlimited
:since:  v0.1.00
		"""

		return self.limit
	#

	def get_percent_remaining(self):
	#
		"""
Returns the percent remaining to be at 100%.

:return: (int) Percent value
:since:  v0.1.00
		"""

		return self.percent_remaining
	#

	def get_row_count(self):
	#
		"""
Returns the number of rows.

:return: (int) Number of rows
:since:  v0.1.00
		"""

		raise NotImplementedException()
	#

	def set_default_sort_definition(self, key, direction):
	#
		"""
Sets the default sort definition to be used.

:param key: Row key to sort
:param direction: Sort direction

:since: v0.1.02
		"""

		if (key not in self.column_definitions): raise ValueException("Given row key is not specified")
		if (direction not in ( Abstract.SORT_ASCENDING, Abstract.SORT_DESCENDING )): raise TypeException("Sort direction given is invalid")

		self.default_sort_definition = { "key": self.column_definitions[key]['sort_key'],
		                                 "direction": direction
		                               }
	#

	def set_limit(self, limit):
	#
		"""
Sets the limit of rows requested.

:param limit: Maximum number of rows requested; -1 for unlimited

:since: v0.1.00
		"""

		self.limit = limit
	#

	def set_offset(self, offset):
	#
		"""
Sets the row offset requested.

:param offset: Row offset requested

:since: v0.1.00
		"""

		self.offset = offset
	#

	def set_sort_context(self, context):
	#
		"""
Sets the sort context to be used.

:param context: Sort context

:since: v0.1.00
		"""

		self.sort_context = context
	#
#

##j## EOF