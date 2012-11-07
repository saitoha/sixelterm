#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ***** BEGIN LICENSE BLOCK *****
# Copyright (C) 2012  Hayaki Saito <user@zuse.jp>
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
# ***** END LICENSE BLOCK *****

import tff
import sixel
try:
    from CStringIO import StringIO
except:
    from StringIO import StringIO


################################################################################
#
# Scanner implementation
#
_MODE_NORMAL = 0
_MODE_PNG    = 1
_MODE_JPEG   = 2

class ImageAwareScanner(tff.Scanner):
    ''' scan input stream and iterate characters '''

    def __init__(self):
        self.__imagebuffer = StringIO()
        self.__mode = _MODE_NORMAL

    def __writeimage(self, value):
        '''
        It seems that Some platform is not possible to disable termios's c_oflag ONLCR. 
        So we replace them with string.replace  
        '''
        self.__imagebuffer.write(value.replace('\x0d\x0a', '\x0a'))

    def assign(self, value, termenc):
        if self.__mode == _MODE_PNG:
            pos = value.find('IEND\xaeB`\x82')
            if pos != -1:
                pos += len('IEND\xaeB`\x82')
                self.__mode = _MODE_NORMAL 
                self.__data = unicode(value[pos:], termenc, 'ignore')
                self.__writeimage(value[:pos])
                sixel.SixelWriter().draw(StringIO(self.__imagebuffer.getvalue()))
                self.__imagebuffer = StringIO()
            else:
                self.__writeimage(value)
        elif self.__mode == _MODE_JPEG:
            pos = value.find('\xff\xd9')
            if pos != -1:
                pos += len('\xff\xd9')
                self.__mode = _MODE_NORMAL 
                self.__data = unicode(value[pos:], termenc, 'ignore')
                self.__writeimage(value[:pos])
                sixel.SixelWriter().draw(StringIO(self.__imagebuffer.getvalue()))
                self.__imagebuffer = StringIO()
            else:
                self.__writeimage(value)
        else:
            pos = value.find('\x89PNG')
            if pos != -1:
                self.__mode = _MODE_PNG 
                self.__data = unicode(value[:pos], termenc, 'ignore')
                self.__writeimage(value[pos:])
                return
            pos = value.find('\xff\xd8\xff')
            if pos != -1:
                self.__mode = _MODE_JPEG 
                self.__data = unicode(value[:pos], termenc, 'ignore')
                self.__writeimage(value[pos:])
                return
            self.__data = unicode(value, termenc, 'ignore')

    def __iter__(self):
        if self.__mode == _MODE_NORMAL:
            for x in self.__data:
                yield ord(x)

