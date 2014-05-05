#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# protocol.py - handles decoding of binary data and the associated object equivalents
#
# For info about protocol and format of messages, please read document
# "WeeChat Relay Protocol", available at:  http://weechat.org/doc/
#
# History:
#
# 2014-05-03, Jacob Melton:
#     initial development
#

import struct
import zlib
import collections
"""
if hasattr(collections, 'OrderedDict'):
    # python >= 2.7
    class WeechatDict(collections.OrderedDict):
        def __str__(self):
            return '{%s}' % ', '.join(['%s: %s' % (repr(key), repr(self[key])) for key in self])
else:
    # python <= 2.6
    WeechatDict = dict
"""

WeechatDict = dict

class Protocol:
    """
    Decode binary message received from WeeChat/relay.
    Returns a WeechatMessage which contains a list of
    all the WeehchatObject variables sent by the relay
    """

    def __init__(self):
        self._obj_cb = {'chr': self._obj_char,
                        'int': self._obj_int,
                        'lon': self._obj_long,
                        'str': self._obj_str,
                        'buf': self._obj_buffer,
                        'ptr': self._obj_ptr,
                        'tim': self._obj_time,
                        'htb': self._obj_hashtable,
                        'hda': self._obj_hdata,
                        'inf': self._obj_info,
                        'inl': self._obj_infolist,
                        'arr': self._obj_array,
                        }

    def _obj_type(self):
        """Read type in data (3 chars)."""
        if len(self.data) < 3:
            self.data = ''
            return ''
        objtype = self.data[0:3].decode()
        self.data = self.data[3:]
        return objtype

    def _obj_len_data(self, length_size):
        """Read length (1 or 4 bytes), then value with this length."""
        if len(self.data) < length_size:
            self.data = ''
            return None
        if length_size == 1:
            length = struct.unpack('B', self.data[0:1])[0]
            self.data = self.data[1:]
        else:
            length = self._obj_int()
        if length < 0:
            return None
        if length > 0:
            value = self.data[0:length]
            self.data = self.data[length:]
        else:
            value = ''
        return value

    def _obj_char(self):
        """Read a char in data."""
        if len(self.data) < 1:
            return 0
        value = struct.unpack('b', self.data[0:1])[0]
        self.data = self.data[1:]
        return value

    def _obj_int(self):
        """Read an integer in data (4 bytes)."""
        if len(self.data) < 4:
            self.data = b''
            return 0
        value = struct.unpack('>i', self.data[0:4])[0]
        self.data = self.data[4:]
        return value

    def _obj_long(self):
        """Read a long integer in data (length on 1 byte + value as string)."""
        value = self._obj_len_data(1)
        if value is None:
            return None
        return int(value)

    def _obj_str(self):
        """Read a string in data (length on 4 bytes + content)."""
        value = self._obj_len_data(4)
        if value is None:
            return None
        if isinstance(value, str):
            return value
        else:
            return value.decode()

    def _obj_buffer(self):
        """Read a buffer in data (length on 4 bytes + data)."""
        return self._obj_len_data(4)

    def _obj_ptr(self):
        """Read a pointer in data (length on 1 byte + value as string)."""
        value = self._obj_len_data(1)
        if value is None:
            return None
        return '0x%s' % value.decode()

    def _obj_time(self):
        """Read a time in data (length on 1 byte + value as string)."""
        value = self._obj_len_data(1)
        if value is None:
            return None
        return int(value)

    def _obj_hashtable(self):
        """Read a hashtable in data (type for keys + type for values + count + items)."""
        type_keys = self._obj_type()
        type_values = self._obj_type()
        count = self._obj_int()
        hashtable = WeechatDict()
        for i in range(0, count):
            key = self._obj_cb[type_keys]()
            value = self._obj_cb[type_values]()
            hashtable[key] = value
        return hashtable

    def _obj_hdata(self):
        """Read a hdata in data."""
        path = self._obj_str()
        keys = self._obj_str()
        count = self._obj_int()
        list_path = path.split('/')
        list_keys = keys.split(',')
        keys_types = []
        dict_keys = WeechatDict()
        for key in list_keys:
            items = key.split(':')
            keys_types.append(items)
            dict_keys[items[0]] = items[1]
        items = []
        for i in range(0, count):
            item = WeechatDict()
            item['__path'] = []
            pointers = []
            for p in range(0, len(list_path)):
                pointers.append(self._obj_ptr())
            for key, objtype in keys_types:
                item[key] = self._obj_cb[objtype]()
            item['__path'] = pointers
            items.append(item)
        return {'path': list_path,
                'keys': dict_keys,
                'count': count,
                'items': items,
                }

    def _obj_info(self):
        """Read an info in data."""
        name = self._obj_str()
        value = self._obj_str()
        return (name, value)

    def _obj_infolist(self):
        """Read an infolist in data."""
        name = self._obj_str()
        count_items = self._obj_int()
        items = []
        for i in range(0, count_items):
            count_vars = self._obj_int()
            variables = WeechatDict()
            for v in range(0, count_vars):
                var_name = self._obj_str()
                var_type = self._obj_type()
                var_value = self._obj_cb[var_type]()
                variables[var_name] = var_value
            items.append(variables)
        return {'name': name, 'items': items}

    def _obj_array(self):
        """Read an array of values in data."""
        type_values = self._obj_type()
        count_values = self._obj_int()
        values = []
        for i in range(0, count_values):
            values.append(self._obj_cb[type_values]())
        return values

    def decode(self, data, separator='\n'):
        """Decode binary data and return list of objects."""
        self.data = data
        size = len(self.data)
        size_uncompressed = size
        uncompressed = None
        # uncompress data (if it is compressed)
        compression = struct.unpack('b', self.data[4:5])[0]
        if compression:
            uncompressed = zlib.decompress(self.data[5:])
            opt1 = struct.pack('>i', len(uncompressed) + 5)
            opt2 = struct.pack('b', 0)
            opt3 = uncompressed
            uncompressed = opt1 + opt2 + opt3
            self.data = uncompressed
        else:
            uncompressed = self.data[:]
        # skip length and compression flag
        self.data = self.data[5:]
        # read id
        msgid = self._obj_str()
        if msgid is None:
            msgid = ''
        # read objects
        objects = WeechatObjects(separator=separator)
        while len(self.data) > 0:
            objtype = self._obj_type()
            value = self._obj_cb[objtype]()
            objects.append(WeechatObject(objtype, value, separator=separator))
        return WeechatMessage(size, size_uncompressed, compression, uncompressed, msgid, objects)

class WeechatObject:
    """
    defines an object from the relay
    each object has a type and a value as defined in the protocol spec
    """
    def __init__(self, objtype, value, separator='\n'):
        self.objtype = objtype;
        self.value = value
        self.separator = separator
        self.indent = '  ' if separator == '\n' else ''
        self.separator1 = '\n%s' % self.indent if separator == '\n' else ''

    def _str_value(self, v):
        if type(v) is str and not v is None:
            return '\'%s\'' % v
        return str(v)

    def _str_value_hdata(self):
        lines = ['%skeys: %s%s%spath: %s' % (self.separator1, self.value['keys'], self.separator, self.indent, self.value['path'])]
        for i, item in enumerate(self.value['items']):
            lines.append('  item %d:%s%s' % ((i + 1), self.separator,
                                             self.separator.join(['%s%s: %s' % (self.indent * 2, key, self._str_value(value)) for key, value in item.items()])))
        return '\n'.join(lines)

    def _str_value_infolist(self):
        lines = ['%sname: %s' % (self.separator1, self.value['name'])]
        for i, item in enumerate(self.value['items']):
            lines.append('  item %d:%s%s' % ((i + 1), self.separator,
                                             self.separator.join(['%s%s: %s' % (self.indent * 2, key, self._str_value(value)) for key, value in item.items()])))
        return '\n'.join(lines)

    def _str_value_other(self):
        return self._str_value(self.value)

    def __str__(self):
        self._obj_cb = {'hda': self._str_value_hdata,
                        'inl': self._str_value_infolist,
                        }
        return '%s: %s' % (self.objtype, self._obj_cb.get(self.objtype, self._str_value_other)())

class WeechatObjects(list):
    """
    essentially a list of WeechatObject variables
    """
    def __init__(self, separator='\n'):
        self.separator = separator

    def __str__(self):
        return self.separator.join([str(weechat_obj) for weechat_obj in self])

class WeechatMessage:
    """
    defines a message from the relay
    key property is objects which is a WeehchatObjects object
    objects is essentially a list of WeechatObject variables
    """
    def __init__(self, size, size_uncompressed, compression, uncompressed, msgid, objects):
        self.size = size
        self.size_uncompressed = size_uncompressed
        self.compression = compression
        self.uncompressed = uncompressed
        self.msgid = msgid
        self.objects = objects

    def __str__(self):
        if self.compression != 0:
            return 'size: %d/%d (%d%%), id=\'%s\', objects:\n%s' % (
                self.size, self.size_uncompressed,
                100 - ((self.size * 100) // self.size_uncompressed),
                self.msgid, self.objects)
        else:
            return 'size: %d, id=\'%s\', objects:\n%s' % (self.size, self.msgid, self.objects)