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

from binascii import hexlify
from math import ceil, floor
from os import urandom

from dNG.data.xml_parser import XmlParser
from dNG.pas.data.binary import Binary
from dNG.pas.data.http.translatable_exception import TranslatableException
from dNG.pas.data.xhtml.formatting import Formatting as XHtmlFormatting
from dNG.pas.data.xhtml.page_links_renderer import PageLinksRenderer
from dNG.pas.data.xhtml.link import Link
from dNG.pas.data.xhtml.oset.file_parser import FileParser
from dNG.pas.data.xhtml.table.abstract import Abstract
from dNG.pas.runtime.type_exception import TypeException
from .module import Module

class Table(Module):
#
	"""
"Table" is used to render a table of rows of columns.

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
Constructor __init__(Table)

:since: v0.1.00
		"""

		Module.__init__(self)

		self.dsd_page_key = "page"
		"""
DSD key used for pagination
		"""
		self.dsd_sort_key = "sort"
		"""
DSD key used for sorting
		"""
		self.page = 1
		"""
Page currently rendered
		"""
		self.page_link_cell = None
		"""
Rendered page link cell
		"""
		self.pages = 1
		"""
Total number of pages available
		"""
		self.sort_direction = None
		"""
Direction of the current sort value
		"""
		self.sort_column_key = ""
		"""
Column key of the current sort value
		"""
		self.table = None
		"""
Table instance
		"""
	#

	def _execute_cell_oset_renderer(self, row, column_definition):
	#
		"""
Renders a cell using the defined OSet template.
		"""

		row_attributes = column_definition['renderer'].get("oset_row_attributes")
		template_name = column_definition['renderer'].get("oset_template_name")

		if (not isinstance(row_attributes, list)): row_attributes = [ column_definition['key'] ]

		content = { }
		for row_attribute in row_attributes: content[row_attribute] = row[row_attribute]

		parser = FileParser()
		parser.set_oset(self.response.get_oset())
		return parser.render(template_name, content)
	#

	def execute_render(self):
	#
		"""
Action for "render_subs"

:since: v0.1.00
		"""

		table = self.context.get("table")
		if (not isinstance(table, Abstract)): raise TranslatableException("core_unknown_error", value = "Missing table instance to render")

		if ("dsd_page_key" in self.context): self.dsd_page_key = self.context['dsd_page_key']
		if ("dsd_sort_key" in self.context): self.dsd_sort_key = self.context['dsd_sort_key']
		self.table = table

		table_id = self.context.get("id")
		self.table_id = ("pas_table_{0}".format(Binary.str(hexlify(urandom(10)))) if (table_id is None) else table_id)

		limit = self.table.get_limit()
		row_count = self.table.get_row_count()

		self.page = (self.context['page'] if ("page" in self.context) else 1)
		self.pages = (1 if (row_count == 0) else ceil(float(row_count) / limit))

		self.table.set_offset(0 if (self.page < 1 or self.page > self.pages) else (self.page - 1) * limit)

		sort_value = self.context.get("sort_value", "")

		if (sort_value != ""):
		#
			self.sort_direction = sort_value[-1:]
			self.sort_column_key = sort_value[:-1]

			self.table.add_sort_definition(self.sort_column_key, self.sort_direction)
		#

		rendered_content = self._render_table_header()
		rendered_content += self._render_table_rows()
		rendered_content += self._render_table_footer()

		self.set_action_result(rendered_content)
	#

	def _get_sort_value(self, column_key):
	#
		"""
Returns the value used to sort the column based on the current one.

:return: (str) Sort value
:since:  v0.1.02
		"""

		_return = ""

		if (self.sort_column_key != column_key): _return = "{0}+".format(column_key)
		elif (self.sort_direction == "+"): _return = "{0}-".format(column_key)

		return _return
	#

	def _render_table_cell(self, row, column_definition):
	#
		"""
Renders the table cell based on the given column definition.

:param row: Row data to render
:param column_definition: Column definition for the cell

:return: (str) Rendered XHTML table cell
:since:  v0.1.00
		"""

		css_text_align_value = column_definition['renderer'].get("css_text_align", "left")
		css_text_align_definition = (None if (css_text_align_value == "left") else "text-align: {0}".format(css_text_align_value))

		_return = "<td></td>"

		callback = None

		td_attributes = { "tag": "td", "attributes": { } }
		if (css_text_align_definition is not None): td_attributes['attributes']['style'] = css_text_align_definition

		if (column_definition['sortable']
		    and self.sort_column_key == column_definition['key']
		   ):
		#
			td_attributes['attributes']['class'] = ("pagetable_column_sorted_asc"
			                                        if (self.sort_direction == "+") else
			                                        "pagetable_column_sorted_desc"
			                                       )
		#

		column_type = column_definition['renderer'].get("type")

		if (column_type == Abstract.COLUMN_RENDERER_CALLBACK):
		#
			if (column_definition['renderer'].get("callback") is None): raise TypeException("Table column renderer callback is invalid")
			callback = column_definition['renderer']['callback']
		#
		elif (column_type == Abstract.COLUMN_RENDERER_SAFE_CONTENT):
		#
			row_data = row[column_definition['key']]
			td_attributes['value'] = XHtmlFormatting.escape("{0}".format(row_data))

			_return = XmlParser().dict_to_xml_item_encoder(td_attributes)
		#
		elif (column_type == Abstract.COLUMN_RENDERER_OSET): callback = self._execute_cell_oset_renderer

		if (callback is not None):
		#
			_return = "{0}{1}</td>".format(XmlParser().dict_to_xml_item_encoder(td_attributes, False),
			                               callback(row, column_definition)
			                              )
		#

		return _return
	#

	def _render_table_footer(self):
	#
		"""
Renders the table page navigation if applicable and footer.

:return: (str) Rendered XHTML table footer
:since:  v0.1.00
		"""

		page_link_cell = ("" if (self.page_link_cell is None) else "\n<tfoot><tr>{0}</tr></tfoot>".format(self.page_link_cell))

		_return = "{0}\n</table>".format(page_link_cell)

		parser = FileParser()
		parser.set_oset(self.response.get_oset())
		_return += parser.render("table.js_footer", { "table_id": self.table_id })

		return _return
	#

	def _render_table_header(self):
	#
		"""
Renders the table header and page navigation if applicable.

:return: (str) Rendered XHTML table header
:since:  v0.1.00
		"""

		table_percent_remaining = self.table.get_percent_remaining()

		xml_parser = XmlParser()

		table_width_percent = 100 - table_percent_remaining

		table_attributes = { "tag": "table",
		                     "attributes": { "class": "pagetable",
		                                     "id": self.table_id,
		                                     "style": "width: {0:d}%; table-layout: auto".format(table_width_percent)
		                                   }
		                   }

		thead_tr_attributes = { "tag": "tr", "attributes": { "class": "pagetable_header_row" } }

		_return = "{0}\n<thead>{1}".format(xml_parser.dict_to_xml_item_encoder(table_attributes, False),
		                                   xml_parser.dict_to_xml_item_encoder(thead_tr_attributes, False),
		                                  )

		column_definitions = self.table.get_column_definitions()

		column_count = len(column_definitions)
		column_percent_addition = int(floor(table_percent_remaining / column_count))
		first_column_percent_addition = table_percent_remaining - (column_percent_addition * column_count)

		for column_key in self.table.get_columns():
		#
			column_definition = column_definitions[column_key]

			css_text_align_value = column_definition['renderer'].get("css_text_align", "left")
			css_text_align_definition = ("" if (css_text_align_value == "left") else "; text-align: {0}".format(css_text_align_value))

			th_attributes = { "tag": "th",
			                  "attributes": { "style": "width: {0:d}%{1}".format(column_definition['size']
			                                                                     + column_percent_addition
			                                                                     + first_column_percent_addition,
			                                                                     css_text_align_definition
			                                                                    )
			                                }
			                }

			if (column_definition['sortable']
			    and self.sort_column_key == column_key
			   ):
			#
				th_attributes['attributes']['class'] = ("pagetable_column_sorted_asc"
				                                        if (self.sort_direction == "+") else
				                                        "pagetable_column_sorted_desc"
				                                       )
			#

			_return += xml_parser.dict_to_xml_item_encoder(th_attributes, False)

			if (column_definition['sortable']):
			#
				sort_value = self._get_sort_value(column_definition['key'])

				link = Link().build_url(Link.TYPE_RELATIVE_URL,
				                        { "__request__": True,
				                          "dsd": { self.dsd_page_key: 1,
				                                   self.dsd_sort_key: sort_value
				                                 }
				                        }
				                       )

				link_attributes = { "tag": "a", "attributes": { "href": link }, "value": column_definition['title'] }

				_return += XmlParser().dict_to_xml_item_encoder(link_attributes, False)
				if (self.sort_column_key == column_key): _return += "<span></span>"
				_return += "</a>"
			#
			else: _return += XHtmlFormatting.escape(column_definition['title'])

			_return += "</th>"

			if (first_column_percent_addition > 0): first_column_percent_addition = 0
		#

		if (self.pages > 1):
		#
			colspan_value = column_count

			page_link_renderer = PageLinksRenderer({ "__request__": True }, self.page, self.pages)
			page_link_renderer.set_dsd_page_key(self.dsd_page_key)
			rendered_links = page_link_renderer.render()

			td_attributes = { "tag": "td",
			                  "attributes": { "class": "pagetable_navigation",
			                                  "colspan": colspan_value
			                                }
			                }

			self.page_link_cell = "{0}{1}</td>".format(xml_parser.dict_to_xml_item_encoder(td_attributes, False),
			                                                   rendered_links
			                                                  )

			_return += "</tr>\n<tr>{0}".format(self.page_link_cell)
		#

		_return += "</tr></thead>"

		return _return
	#

	def _render_table_row(self, row):
	#
		"""
Renders the table row.

:param row: Row data to render

:return: (str) Rendered XHTML table row
:since:  v0.1.00
		"""

		_return = "\n<tr>"

		column_definitions = self.table.get_column_definitions()

		for column_key in self.table.get_columns():
		#
			_return += self._render_table_cell(row, column_definitions[column_key])
		#

		_return += "</tr>"

		return _return
	#

	def _render_table_rows(self):
	#
		"""
Renders the table rows.

:return: (str) Rendered XHTML table rows
:since:  v0.1.00
		"""

		_return = "<tbody>"
		for row in self.table: _return += self._render_table_row(row)
		_return += "</tbody>"

		return _return
	#
#

##j## EOF