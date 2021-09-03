# importer.py
#
# Copyright 2020 brombinmirko <send@mirko.pm>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk

from ..backend.backup import RunnerBackup

from ..widgets.importer import ImporterEntry


@Gtk.Template(resource_path='/com/usebottles/bottles/importer.ui')
class ImporterView(Gtk.ScrolledWindow):
    __gtype_name__ = 'ImporterView'

    # region Widgets
    list_prefixes = Gtk.Template.Child()
    btn___find_prefixes = Gtk.Template.Child()
    btn_import_config = Gtk.Template.Child()
    btn_import_full = Gtk.Template.Child()
    # endregion

    def __init__(self, window, **kwargs):
        super().__init__(**kwargs)

        # common variables and references
        self.window = window
        self.manager = window.manager

        # connect signals
        self.btn___find_prefixes.connect("pressed", self.__find_prefixes)
        self.btn_import_full.connect("pressed", self.__import_full_bck)

    def __find_prefixes(self, widget):
        '''
        This function remove all entries from the list_prefixes, ask the
        manager to find all prefixes in the system and add them to the list
        '''
        for w in self.list_prefixes.get_children():
            w.destroy()

        wineprefixes = self.manager.__find_prefixes()
        if len(wineprefixes) > 0:
            for wineprefix in wineprefixes:
                self.list_prefixes.add(ImporterEntry(self.window, wineprefix))

    def __import_full_bck(self, widget):
        '''
        This function show a dialog to the user, from wich it can choose an
        archive backup to import into Bottles. It support only .tar.gz files
        as Bottles export bottles in this format. Once selected, it will
        be imported.
        '''
        file_dialog = Gtk.FileChooserNative.new(
            _("Choose a backup archive"),
            self.window,
            Gtk.FileChooserAction.OPEN
        )

        filter_tar = Gtk.FileFilter()
        filter_tar.set_name(".tar.gz")
        filter_tar.add_pattern("*.tar.gz")
        file_dialog.add_filter(filter_tar)

        response = file_dialog.run()

        if response == -3:
            RunnerBackup().import_backup_bottle(
                self.window,
                "full",
                file_dialog.get_filename()
            )

        file_dialog.destroy()
