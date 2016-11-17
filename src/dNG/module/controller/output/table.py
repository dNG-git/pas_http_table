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

from dNG.data.http.translatable_error import TranslatableError
from dNG.runtime.value_exception import ValueException

from .module import Module
from .table_mixin import TableMixin

class Table(Module, TableMixin):
    """
"Table" is used to render a table of rows as a block action.

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
Constructor __init__(Table)

:since: v0.2.00
        """

        Module.__init__(self)
        TableMixin.__init__(self)
    #

    def execute_render(self):
        """
Action for "render"

:since: v0.2.00
        """

        if (self._is_primary_action()): raise TranslatableError("core_access_denied", 403)

        self.table = self.context.get("object")

        if ("dsd_page_key" in self.context): self.dsd_page_key = self.context['dsd_page_key']
        if ("dsd_sort_key" in self.context): self.dsd_sort_key = self.context['dsd_sort_key']

        if ("options_api_service" in self.context):
            self.table_options_api_service = self.context['options_api_service']
            if ("options_api_dsd_context" in self.context): self.table_options_api_dsd_context = self.context['options_api_dsd_context']
        #

        self.table_id = self.context.get("id")

        if (self.table_options_api_service is not None
            and self.table_id is None
           ): raise ValueException("Tables with dynamic options need a unique table ID")

        self.page = self.context.get("page", 1)
        self.page_limit = self.context.get("page_limit", 0)

        sort_value = self.context.get("sort_value", "")

        if (sort_value != ""):
            self.sort_direction = sort_value[-1:]
            self.sort_column_key = sort_value[:-1]
        #

        self.set_action_result(self._render_table())
    #
#
