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

from dNG.module.controller.services.abstract_dom_editor import AbstractDomEditor
from dNG.runtime.not_implemented_exception import NotImplementedException

class Abstract(AbstractDomEditor):
#
	"""
"Abstract" is used to handle dynamic table options.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: table
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
	"""

	OSET_TEMPLATE_NAME = None
	"""
OSet template name used to render the table options.
	"""

	def execute_index(self):
	#
		"""
Action for "index"

:since: v0.2.00
		"""

		self.execute_show()
	#

	def execute_show(self):
	#
		"""
Action for "show"

:since: v0.2.00
		"""

		if (self.__class__.OSET_TEMPLATE_NAME is None): raise NotImplementedException()

		self._set_replace_dom_oset_result(self.__class__.OSET_TEMPLATE_NAME, self._get_show_content())
	#

	def _get_show_content(self):
	#
		"""
Returns the OSet content for the table options.

:return: (dict) OSet content
:since:  v0.2.00
		"""

		return { }
	#
#

##j## EOF