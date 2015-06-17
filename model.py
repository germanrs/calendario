# -*- coding: utf-8 -*-
#
#Copyright (C) 2010-2012, Yader Velasquez
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gtk
import pygtk
from gettext import gettext as _
import logging
import gobject
import calendario
log = logging.getLogger('Calendario-Model-Log')

class ComboBoxModel(object):
    '''Models for ComboBox'''
    def __init__(self):

        self.category = [_("Personal"), _("Work"), _("Study")]
        self.priority = [_("Low"), _("Medium"), _("High")]

    def get_category_model(self):
        '''return the model for the category ComboBox'''
        model = gtk.ListStore(str)
        for item in self.category:
            model.append([item])

        return model

    def get_priority_model(self):
        '''return the model for the categoty ComboBox'''
        model = gtk.ListStore(str)
        for item in self.priority:
            model.append([item])
            
        return model

class TasksModel(object):
    '''Model for tasks treeview'''
    def __init__(self, tasks_list):
        self.tasks =  tasks_list

    def get_model(self):
        model = gtk.ListStore(
                gobject.TYPE_INT,
                gobject.TYPE_STRING,
                gobject.TYPE_STRING,
                gobject.TYPE_STRING,
                gobject.TYPE_BOOLEAN)

        for o in self.tasks:

            c = o.get_category()
            if c == 0:
                category = _("Personal")
            elif c == 1:
                category = _("Work")
            elif c == 2:
                category = _("Study")
            else:
                category = ''
            
            p = o.get_priority()
            if p == 0:
                priority = _("Low")
            elif p == 1:
                priority = _("Medium")
            elif p == 2:
                priority = _("High")
            else:
                priority = ''

            if o.get_complete() == 1:
                status = True
                task = calendario.strike_string(o.get_task())
            else:
                status = False
                task = o.get_task()

            model.append([o.get_task_id(), task, category, priority, status])
        return model
