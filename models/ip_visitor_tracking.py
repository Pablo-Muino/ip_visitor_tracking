from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import logging

# Configuramos el logger
_logger = logging.getLogger(__name__)

class IpVisitorTracker(models.Model):
    _name = 'ip.visitor.tracker'
    _description = 'Tracker del cliente mediante su Ip'
    _rec_name = 'ip_address'

    # Campos que se almacenarán en la base de datos
    ip_address = fields.Char(string='Dirección IP', required=True)
    country = fields.Char(string='País')
    city = fields.Char(string='Ciudad')
    latitude = fields.Float(string='Latitud')
    longitude = fields.Float(string='Longitud')
    isp = fields.Char(string='ISP')
    organization = fields.Char(string='Organización')
    visit_time = fields.Datetime(string='Hora de Visita', default=fields.Datetime.now)
    
    api_key = fields.Char(string="API Key", required=True)
    
    # Método para obtener la geolocalización
    def fetch_geolocation(self):
        for record in self:
            # Formar la URL con la IP y la clave de la API
            url = f"https://api.ipgeolocation.io/ipgeo?apiKey={record.api_key}&ip={record.ip_address}"

            try:
                # Realizar la solicitud HTTP GET
                response = requests.get(url)
                
                # Verificar si la respuesta fue exitosa
                if response.status_code == 200:
                    data = response.json()
                    
                    # Asignar los datos obtenidos a los campos correspondientes
                    record.country = data.get('country_name', '')
                    record.city = data.get('city', '')
                    record.latitude = data.get('latitude', 0.0)
                    record.longitude = data.get('longitude', 0.0)
                    record.isp = data.get('isp', '')
                    record.organization = data.get('organization', '')
                else:
                    raise ValueError("Error al obtener los datos de geolocalización. Código de estado: " + str(response.status_code))
            except requests.RequestException as e:
                # Manejo de excepciones para errores en la solicitud HTTP
                raise ValueError(f"Error de conexión con la API: {str(e)}")
    
    # Método para crear registros desde la vista de formulario (solo si es necesario)
    def create_visitor_record(self, ip_address, api_key):
        self.create({
            'ip_address': ip_address,
            'api_key': api_key,
        }).fetch_geolocation()
    
    def _is_valid_ip(self, ip):
        # Expresión regular para validar una dirección IP (IPv4)
        ip_pattern = r'^([0-9]{1,3}\.){3}[0-9]{1,3}$'
        return bool(re.match(ip_pattern, ip))
    
    def write(self, vals):
        # Verificamos si el usuario tiene permisos de administrador
        self.check_admin_permission()
        
        # Validamos si la IP y la API Key están presentes y correctas en la actualización
        if 'ip_address' in vals and not self._is_valid_ip(vals.get('ip_address')):
            raise ValueError("La dirección IP proporcionada no es válida.")
        
        return super(Visitor, self).write(vals)

    @api.model
    def check_admin_permission(self):
        if not self.env.user.has_group('base.group_system'):
            raise PermissionError("No tienes permisos suficientes para acceder a esta información.")
        
    @api.constrains('ip_address')
    def _check_ip_address(self):
        for record in self:
            if not self._is_valid_ip(record.ip_address):
                raise ValueError("La dirección IP proporcionada no es válida.")