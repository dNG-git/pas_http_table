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

from dNG.pas.runtime.value_exception import ValueException
from .abstract import Abstract as _Abstract
from .custom_row import CustomRow

class Custom(_Abstract):
#
	"""
"Custom" defines a table based on manually defined rows.

:author:     direct Netware Group
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: table
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self):
	#
		"""
Constructor __init__(Custom)

:since: v0.1.00
		"""

		_Abstract.__init__(self)

		self.row_count = None
		"""
Manual set row count
		"""
		self.rows = [ ]
		"""
List of rows
		"""
	#

	def __iter__(self):
	#
		"""
python.org: Return an iterator object.

:return: (object) Iterator object
:since:  v0.1.00
		"""

		return iter(self.rows)
	#

	def add_row(self, **kwargs):
	#
		"""
Adds row data to this table.

:since: v0.1.00
		"""

		self.rows.append(CustomRow(kwargs))
	#

	def get_row_count(self):
	#
		"""
Returns the number of rows.

:return: (int) Number of rows
:since:  v0.1.00
		"""

		if (self.row_count is None): self.row_count = len(self.rows)
		return self.row_count
	#

	def set_row_count(self, row_count):
	#
		"""
Sets the row count.

:param row_count: Number of rows

:since: v0.1.00
		"""

		self.row_count = row_count
	#
#

##j## EOF