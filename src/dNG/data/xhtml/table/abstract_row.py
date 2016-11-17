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

from dNG.runtime.not_implemented_exception import NotImplementedException

class AbstractRow(object):
    """
"AbstractRow" provides properties for column keys and is used to access row
columns in a standardized way.

:author:     direct Netware Group et al.
:copyright:  (C) direct Netware Group - All rights reserved
:package:    pas.http
:subpackage: table
:since:      v0.2.00
:license:    https://www.direct-netware.de/redirect?licenses;mpl2
             Mozilla Public License, v. 2.0
    """

    def get(self, key, default = None):
        """
python.org: Return the value for key if key is in the dictionary, else
default.

:param key: Key
:param default: Default return value

:return: (mixed) Value
:since:  v0.2.00
        """

        _return = default

        try: _return = self[key]
        except KeyError: pass

        return _return
    #

    def __getitem__(self, key):
        """
python.org: Called to implement evaluation of self[key].

:param name: Attribute name

:return: (mixed) Attribute value
:since:  v0.2.00
        """

        raise NotImplementedException()
    #
#
