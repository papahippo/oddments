#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Remove 'module' files from tree of assets. I'm subclassing the existing Walker class for this,
even though I'm intending to adopt a better approach to such tasks 'some time soon'.
"""
import os

from walker import Walker

class WalkAside(Walker):

    name_ =  "selective walker/renamer"
    myExts = ('.py',)
    prefix_ = 'hidden-'

    def handle_item(self, root_, item_name, is_dir):

        if is_dir or not Walker.handle_item(self, root_, item_name, is_dir):
            return None
        if item_name not in ('musicParts.py',):
            return False
        self.vprint(1, f"os.rename('{self.full_source_name}', '{self.full_dest_name}')")
        os.rename(self.full_source_name, self.full_dest_name)
        return True  # stub!


if __name__ == '__main__':
    WalkAside().main()
