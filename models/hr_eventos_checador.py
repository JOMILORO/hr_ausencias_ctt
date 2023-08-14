# -*-coding:utf-8 -*-
from odoo import fields, models, api

class EventosChecador(models.Model):
    _name = 'hr.eventos.checador'
    _description = 'Eventos de checador'
    _order = 'departamento_id,pin,fecha_hora desc'

    name = fields.Char(string='Movimiento', required=False, index=True, copy=False, default='Nuevo')
    active = fields.Boolean(string='Activo', default=True)
    empleado_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Empleado",
        required=True,
        copy=True,
        index=True
    )
    departamento_id = fields.Many2one(
        comodel_name="hr.department",
        string="Departamento",
        related="empleado_id.department_id",
        store=True
    )
    estado = fields.Selection(string="Estado", selection=[
        ('0', 'Entrada'),
        ('1', 'Salida'),
        ('2', 'Salida Temporal'),
        ('3', 'Regreso'),
        ('4', 'Entrada T.E.'),
        ('5', 'Salida T.E.')
    ], required=True)
    fecha_hora = fields.Datetime(string="Fecha / Hora", required=True)
    pin = fields.Char(string="Código NIP", required=False, store=True, index=True, related="empleado_id.pin")
    checador_id = fields.Many2one(
        comodel_name='hr.checador.asistencia',
        string='Checador',
        required=True)
    tipo_registro = fields.Selection(string="Tipo de registro", selection=[('1', 'Normal')], required=False)
    numero_identificacion = fields.Char(string="Código nómina", related="empleado_id.identification_id", store=True,
                                        index=True)
    empleado_categoria = fields.Many2many(
        'hr.employee.category',
        'employee_category_rel',
        'emp_id', 'category_id',
        string='Emp. categoría', related="empleado_id.category_ids")
    registro = fields.Selection(string="Registro", selection=[
        ('0', 'Clave'),
        ('1', 'Huella')
    ], required=False, default='Huella')
    identificador_registro = fields.Float(string="Identificador", required=False, index=True)

    @api.model
    def create(self, values):
        # Add code here
        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.hr.eventos.checador')
        values['name'] = correlativo
        return super(EventosChecador, self).create(values)