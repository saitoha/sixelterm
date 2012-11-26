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
    from cStringIO import StringIO
except:
    from StringIO import StringIO


################################################################################
#
# Scanner implementation
#
_MODE_NORMAL = 0
_MODE_PNG    = 1
_MODE_JPEG   = 2

_JPEG_SOI = '\xff\xd8'
_JPEG_EOI = '\xff\xd9'

_PNG_IEND = ''
class ImageAwareScanner(tff.Scanner):
    ''' scan input stream and iterate characters '''

    def __init__(self):
        self.__imagebuffer = StringIO()
        self.__mode = _MODE_NORMAL
        self.__writer = sixel.SixelWriter()

    def __writeimage(self, value):
        self.__imagebuffer.write(value)

    def __convert(self):
        try:
            data = self.__imagebuffer.getvalue()
            self.__writer.draw(StringIO(data))
        except:
            self.__data += 'cannot identify image file\n'
        self.__imagebuffer = StringIO()

    def assign(self, value, termenc):
        self.__termenc = termenc
        if self.__mode == _MODE_PNG:
            pos = value.find('IEND\xaeB`\x82')
            if pos != -1:
                pos += len('IEND\xaeB`\x82')
                self.__mode = _MODE_NORMAL 
                self.__data = value[pos:]
                self.__writeimage(value[:pos])
                self.__convert()
            else:
                self.__writeimage(value)
        elif self.__mode == _MODE_JPEG:
            pos = value.find(_JPEG_EOI)
            if pos != -1:
                pos += len(_JPEG_EOI)
                if pos != len(value) and (value[pos] == '\x00' or value[pos] == '\xff'):
                    self.__writeimage(value)
                else:
                    self.__mode = _MODE_NORMAL 
                    self.__data = value[pos:]
                    self.__writeimage(value[:pos])
                    self.__convert()
            else:
                self.__writeimage(value)
        else:
            pos = value.find('\x89PNG')
            if pos != -1:
                self.__mode = _MODE_PNG 
                self.__cr = False
                self.__data = value[:pos]
                self.__writeimage(value[pos:])
                return
            pos = value.find(_JPEG_SOI)
            if pos != -1:
                self.__mode = _MODE_JPEG 
                self.__cr = False
                self.__data = value[:pos]
                self.__writeimage(value[pos:])
                return
            self.__data = value

    def __iter__(self):
        if self.__mode == _MODE_NORMAL:
            for x in unicode(self.__data, self.__termenc, 'ignore'):
                yield ord(x)

