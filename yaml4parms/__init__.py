""" yaml4parms

.. module:: yaml4parms
    :synopsis: tool to mix yaml structured schema description with actual text based parameters files

.. moduleauthor:: Marc Portier <marc.portier@gmail.com>

"""

from .tool import ParameterDescription, read
import logging

__all__ = ['read', 'ParameterDescription']

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
