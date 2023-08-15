# -*- coding:utf-8 -*-

import logging
import io
import base64
from datetime import datetime, timedelta
from odoo import fields, models, api, exceptions

logger = logging.getLogger(__name__)


class HRUploadFileTimeClockWizard(models.TransientModel):
    _name = 'hr.upload.file.time.clock.wizard'
    _description = 'Wizard subir archivo checador ZK'

    upload_file = fields.Binary(string="Subir fichero", required=True)
    file_name = fields.Char(string="Nombre del fichero", required=False)
    checador_id = fields.Many2one(
        comodel_name='hr.checador.asistencia',
        string='Checador',
        required=True
    )
    adicionar_horas = fields.Integer(string="Adicionar horas", required=True, default=6)

    def import_file_time_clock(self):
        if self.file_name and self.checador_id:
            checador_id = self.checador_id.id
            if '.dat' not in self.file_name:
                raise exceptions.ValidationError('El archivo debe ser un .dat')
            file = self.read_file_from_binary(self.upload_file)
            lines = file.split('\n')
            for line in lines:
                elements = line.split('\t')
                if len(elements) > 1:
                    empleado = self.env['hr.employee'].search([
                        ('pin', '=', int(elements[0]))
                    ], order='identification_id desc', limit=1)
                    if empleado:
                        fecha_hora_registro = datetime.strptime(elements[1], "%Y-%m-%d %H:%M:%S")
                        identificador_registro = int(fecha_hora_registro.strftime("%Y%m%d%H%M%S")) + int(elements[0])
                        departamento_id = empleado.department_id.id
                        numero_identificacion = empleado.identification_id
                        evento = self.env['hr.eventos.checador'].search([
                            ('identificador_registro', '=', identificador_registro)
                        ], limit=1)
                        if not evento:
                            self.env['hr.eventos.checador'].create({
                                'empleado_id': empleado.id,
                                'estado': elements[3],
                                'fecha_hora': fecha_hora_registro + timedelta(hours=self.adicionar_horas),
                                'pin': elements[0],
                                'checador_id': checador_id,
                                'tipo_registro': '1',
                                'registro': elements[4],
                                'identificador_registro': identificador_registro,
                                'departamento_id': departamento_id,
                                'numero_identificacion': numero_identificacion
                            })

    def read_file_from_binary(self, file):
        try:
            with io.BytesIO(base64.b64decode(file)) as f:
                f.seek(0)
                return f.read().decode('UTF-8')
        except Exception as e:
            print(str(e))
            raise e
