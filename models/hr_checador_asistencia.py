# -*-coding:utf-8 -*-
from odoo import fields, models, api

class ChecadorAsistencia(models.Model):
    _name = 'hr.checador.asistencia'
    _description = 'Checador  de asistencia'
    _order = 'name'

    name = fields.Char(string='Nombre', required=True, index=True)
    ubicacion = fields.Char(string="Ubicación", required=False)
    active = fields.Boolean(string='Activo', default=True)
    descripcion = fields.Text(string='Anotaciones', required=False, copy=False)
    grupo_checador_id = fields.Many2one(
        comodel_name="hr.checador.asistencia.grupo",
        string="Grupo",
        required=False
    )

    def copy(self, default=None):
        default = dict(default or {})
        default['name'] = self.name + ' (Copia)'
        return super(ChecadorAsistencia, self).copy(default)

    _sql_constraints = [
        ('nombre_checador_unique',
         'UNIQUE(name)',
         "El nombre del checador de ser único, busque o vuelva " +
         "a intentarlo si no lo encuentra por favor verifique que el nombre del checador se encuentre activo."),
    ]

class ChecadorAsistenciaGrupo(models.Model):
    _name = 'hr.checador.asistencia.grupo'
    _description = 'Grupo de checadores  de asistencia'
    _order = 'name'

    name = fields.Char(string="Nombre de grupo", required=True, index=True)

    _sql_constraints = [
        ('nombre_grupo_unique',
         'UNIQUE(name)',
         "El nombre del grupo para checadores debe de ser único, vuelva a intentarlo con otro nombre por favor"),
    ]