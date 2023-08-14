# -*- coding:utf-8 -*-
{
    'name': 'Ausencias Confetex',
    'version': '1.0',
    'depends': [
        'base',
        'hr',
        'hr_holidays',
        'hr_attendance',
        'contacts',
        'base_automation',
        'mail',
    ],
    'author': 'José Miguel López Roano',
    'website': 'https://www.confetex.com',
    'summary': 'Adaptación de los módulos Asistencia y Ausencias para trabajar con requerimientos Confetex.',
    'category': 'Human Resources/Time Off',
    'description': '''Modulo para el control y administración de permisos, ausencias y asistencias de empldeados''',
    'data': [
        'data/secuencia.xml',
        'security/ir.model.access.csv',
        'views/hr_menu.xml',
        'views/hr_checador_asistencia_view.xml',
        'views/hr_empleado_ausencia_view.xml',
        'views/hr_eventos_checador_view.xml',
        'wizard/hr_upload_file_time_clock_wizard_view.xml',
    ],
}