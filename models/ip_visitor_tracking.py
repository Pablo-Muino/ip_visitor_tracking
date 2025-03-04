from odoo import models, fields
from odoo.exceptions import UserError
import requests
import logging

# Configuramos el logger
_logger = logging.getLogger(__name__)

class IpVisitorTracker(models.Model):
    _name = 'ip.visitor.tracker'
    _description = 'Tracker del cliente mediante su Ip'
    _rec_name = 'city'