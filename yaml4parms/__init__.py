""" yaml4parms

.. module:: yaml4parms
    :synopsis: tool to mix yaml structured schema description with actual text based parameters files

.. moduleauthor:: Marc Portier <marc.portier@gmail.com>

"""

from .tool import MyModel
import logging

__all__ = ['MyModel']

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
