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

from dNG.pas.data.xhtml.formatting import Formatting
from .abstract_field import AbstractField
from .read_only_field_mixin import ReadOnlyFieldMixin

class InfoTableField(ReadOnlyFieldMixin, AbstractField):
#
	"""
"InfoTableField" provides a table for the field content.

:author:     direct Netware Group
:copyright:  direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: table
:since:      v0.1.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	def __init__(self, name = None):
	#
		"""
Constructor __init__(InfoTableField)

:param name: Form field name

:since: v0.1.00
		"""

		AbstractField.__init__(self, name)
		ReadOnlyFieldMixin.__init__(self)

		self.table = None
		"""
Table used for the field content
		"""
	#

	def _get_content(self):
	#
		"""
Returns the field content.

:return: (str) Field content
:since:  v0.1.00
		"""

		return Formatting.escape(AbstractField._get_content(self))
	#

	def get_type(self):
	#
		"""
Returns the field type.

:return: (str) Field type
:since:  v0.1.00
		"""

		return "infotable"
	#

	def render(self):
	#
		"""
Renders the given field.

:return: (str) Valid XHTML form field definition
:since:  v0.1.00
		"""

		context = { "title": Formatting.escape(self.get_title()),
		            "content": self._get_content(),
		            "table": { "table": self.table },
		            "error_message": ("" if (self.error_data is None) else Formatting.escape(self.get_error_message()))
		          }

		return self._render_oset_file("table/form/info_table", context)
	#

	def set_table(self, table):
	#
		"""
Sets the table used for the field content.

:param link: Link URL

:since: v0.1.00
		"""

		self.table = table
	#
#

##j## EOF