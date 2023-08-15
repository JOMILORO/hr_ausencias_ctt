# -*-coding:utf-8 -*-

import logging

from odoo import fields, models, api
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class EmpleadoAusencia(models.Model):
    _inherit = "hr.employee"

    apellido_checador = fields.Char(string="Apellido en checador", copy=False, required=False)
    checador_nombre = fields.Char(string="Nombre en checador", copy=False, required=False)
    estado_checador = fields.Selection(string='Estado checador', selection=[
        ('agregar', 'Agregar'),
        ('alta', 'Alta'),
        ('eliminar', 'Eliminar'),
        ('pendiente', 'Pendiente'),
    ], required=False, default='agregar')
    fecha_despido = fields.Date(string="Fecha despido", required=False)
    fecha_empleo = fields.Date(string="Fecha de empleo", required=True)
    tipo_usuario_checador = fields.Selection(string='Tipo de usuario', selection=[
        ('administrador', 'Administrador'),
        ('usuario', 'Usuario'),
    ], required=True, default='usuario')
    checador_id = fields.Many2one(
        comodel_name='hr.checador.asistencia',
        string='Checador',
        required=False)
    ubicacion = fields.Char(string="Ubicación", related="checador_id.ubicacion")
    grupo_checador_id = fields.Many2one(
        comodel_name="hr.checador.asistencia.grupo",
        string="Grupo",
        related="checador_id.grupo_checador_id",
        required=False
    )

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        recs = self.browse()
        if not recs:
            recs = self.search(['|', ('identification_id', operator, name), ('name', operator, name)] + args,
                               limit=limit)
        return recs.name_get()