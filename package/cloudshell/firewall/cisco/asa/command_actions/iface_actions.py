#!/usr/bin/python
# -*- coding: utf-8 -*-

from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.firewall.cisco.asa.command_templates import iface as iface_command_template


class IFaceActions(object):
    def __init__(self, cli_service, logger):
        """ Add remove vlan

        :param cli_service: config mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """

        self._cli_service = cli_service
        self._logger = logger

    def get_port_name(self, port):
        """ Get port name from port resource full address

        :param port: port resource full address (192.168.1.1/0/34)
        :return: port name (FastEthernet0/23)
        :rtype: string
        """

        if not port:
            err_msg = 'Failed to get port name.'
            self._logger.error(err_msg)
            raise Exception('CiscoConnectivityOperations: get_port_name', err_msg)

        temp_port_name = port.split('/')[-1]
        if 'port-channel' not in temp_port_name.lower():
            temp_port_name = temp_port_name.replace('-', '/')

            self._logger.info('Interface name validation OK, portname = {0}'.format(temp_port_name))
        return temp_port_name

    def get_current_interface_config(self, port_name, action_map=None, error_map=None):
        """Retrieve current interface configuration

        :param port_name:
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        :return: str
        """

        return CommandTemplateExecutor(self._cli_service,
                                       iface_command_template.SHOW_RUNNING,
                                       action_map=action_map,
                                       error_map=error_map).execute_command(port_name=port_name)

    def enter_iface_config_mode(self, port_name):
        """ Enter configuration mode for specific interface

        :param port_name: interface name
        :return:
        """

        CommandTemplateExecutor(self._cli_service,
                                iface_command_template.CONFIGURE_INTERFACE).execute_command(port_name=port_name)

    def clean_interface_switchport_config(self, current_config, action_map=None, error_map=None):
        """ Remove current switchport configuration from interface

        :param current_config: current interface configuration
        :param action_map: actions will be taken during executing commands, i.e. handles yes/no prompts
        :param error_map: errors will be raised during executing commands, i.e. handles Invalid Commands errors
        """

        self._logger.debug("Start cleaning interface switchport configuration")

        for line in current_config.splitlines():
            if line.strip(" ").startswith('switchport '):
                CommandTemplateExecutor(self._cli_service,
                                        iface_command_template.NO, action_map=action_map,
                                        error_map=error_map).execute_command(command=line.strip(' '))

                self._logger.debug("Completed cleaning interface switchport configuration")
