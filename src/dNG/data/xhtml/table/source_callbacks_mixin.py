# -*- coding: utf-8 -*-

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

class SourceCallbacksMixin(object):
    """
"SourceCallbacksMixin" provides methods to receive the rows from an external
source with registered callbacks.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: table
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def __init__(self):
        """
Constructor __init__(SourceCallbacksMixin)

:since: v0.2.00
        """

        self.source_row_count_callback = None
        """
Callback to receive the total number of rows available.
        """
        self.source_rows_callback = None
        """
Callback to receive the iterator source from.
        """
    #

    def set_source_callbacks(self, rows_callback, row_count_callback):
        """
Sets the callbacks to receive the iterator source from.

:param rows_callback: It is called with "offset" and "limit" arguments to
                      get a list-like result to iterate over.
:param row_count_callback: The count callback is used to receive the number
                           of rows available.

:since: v0.2.00
        """

        self.source_rows_callback = rows_callback
        self.source_row_count_callback = row_count_callback
    #
#
