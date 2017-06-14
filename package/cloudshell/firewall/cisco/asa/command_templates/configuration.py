# !/usr/bin/python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from cloudshell.cli.command_template.command_template import CommandTemplate

COPY = CommandTemplate('copy [/noconfirm {noconfirm}] {src} {dst}',
                       action_map=OrderedDict({
                           r'\[confirm\]': lambda session, logger: session.send_line('', logger),
                           r'\(y/n\)': lambda session, logger: session.send_line('y', logger),
                           r'[Oo]verwrit+e': lambda session, logger: session.send_line('y', logger),
                           r'\([Yy]es/[Nn]o\)': lambda session, logger: session.send_line('yes', logger)}))

DEL = CommandTemplate('del {target}', action_map=OrderedDict(
    {'[confirm]': lambda session, logger: session.send_line('', logger),
     '\?': lambda session, logger: session.send_line('', logger)}))

CONFIGURE_REPLACE = CommandTemplate('configure replace {path}',
                                    action_map=OrderedDict({
                                        '[\[\(][Yy]es/[Nn]o[\)\]]|\[confirm\]': lambda session,
                                                                                       logger: session.send_line('yes',
                                                                                                                 logger),
                                        '\(y\/n\)': lambda session, logger: session.send_line('y', logger),
                                        '[\[\(][Nn]o[\)\]]': lambda session, logger: session.send_line('y', logger),
                                        '[\[\(][Yy]es[\)\]]': lambda session, logger: session.send_line('y', logger),
                                        '[\[\(][Yy]/[Nn][\)\]]': lambda session, logger: session.send_line('y', logger),
                                        'overwrit+e': lambda session, logger: session.send_line('yes', logger)}),
                                    error_map=OrderedDict({
                                        "[Rr]ollback\s*[Dd]one|(?<=%).*(not.*|in)valid.*(?=\n)":
                                            Exception("Configure_Replace",
                                                      "Configure replace completed with error"),
                                        "[Ii]nvalid\s*([Ii]nput|[Cc]ommand)|[Cc]ommand rejected":
                                            Exception('Configure_Replace', 'Override mode is not supported')
                                    }))

WRITE_ERASE = CommandTemplate('write erase',
                              action_map=OrderedDict({
                                  '[\[\(][Yy]es/[Nn]o[\)\]]|\[confirm\]': lambda session,
                                                                                 logger: session.send_line('yes',
                                                                                                           logger),
                                  '\(y\/n\)': lambda session, logger: session.send_line('y', logger),
                                  '[\[\(][Nn]o[\)\]]': lambda session, logger: session.send_line('y', logger),
                                  '[\[\(][Yy]es[\)\]]': lambda session, logger: session.send_line('y', logger),
                                  '[\[\(][Yy]/[Nn][\)\]]': lambda session, logger: session.send_line('y', logger),
                              }))

RELOAD = CommandTemplate("reload", action_map=OrderedDict(
    {'[\[\(][Yy]es/[Nn]o[\)\]]': lambda session, logger: session.send_line('yes', logger),
     '\[confirm\]': lambda session, logger: session.send_line('', logger),
     '\(y\/n\)|continue': lambda session, logger: session.send_line('y', logger),
     'reload': lambda session, logger: session.send_line('', logger),
     '[\[\(][Yy]/[Nn][\)\]]': lambda session, logger: session.send_line('y', logger)
     }))

CONSOLE_RELOAD = CommandTemplate("reload")
