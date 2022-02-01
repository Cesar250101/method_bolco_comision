# -*- coding: utf-8 -*-

from calendar import month
from datetime import datetime, timedelta
from odoo import models, fields, api


class Productos(models.Model):
    _inherit = 'product.template'

    producto_origen = fields.Selection(string='Origen', selection=[('nacional', 'Nacional'), ('importado', 'Importado'),])



class PorcComision(models.Model):
    _name = 'method_bolco_comision.por_comision'
    _description = 'Porcentajes de comisión'

    producto_origen = fields.Selection(string='Origen', selection=[('nacional', 'Nacional'), ('importado', 'Importado'),])
    comision_porcentaje = fields.Float(string='Porcentaje Comisión')
    comision_haber = fields.Many2one(comodel_name='hr.salary.rule', string='Haber Nómina')
    
    
class Nomina(models.Model):
    _inherit = 'hr.payslip'


    @api.one
    def compute_sheet(self):
        contrato_id = self.env['hr.contract'].search([('employee_id', '=', self.employee_id.id), ('state', '=', 'open')])
        mes_anterior=self.get_created_after_date(self.date_to,45)
        fecha_desde = str(mes_anterior)
        fecha_desde=fecha_desde[:8]
        fecha_desde+="16"
        fecha_hasta = str(self.date_to)
        fecha_hasta=fecha_hasta[:8]
        fecha_hasta+="15"
        hastaStr = datetime.strptime(fecha_hasta, '%Y-%m-%d')
        desdeStr = datetime.strptime(fecha_desde, '%Y-%m-%d')
        comision = 0
        domain = [
                ('state', 'in', ['open','paid']),
                ('date_invoice', '>=', fecha_desde),
                ('date_invoice', '<=', fecha_hasta),
                ('user_id','=',self.employee_id.user_id.id),
                ('type','=','out_invoice'),
                ('sii_code','in',['33','34','56','39','61'])
            ]
        porc_nacional=self.env['method_bolco_comision.por_comision'].search([('producto_origen','=','nacional')],limit=1)
        porc_importado=self.env['method_bolco_comision.por_comision'].search([('producto_origen','=','importado')],limit=1)

        porc_nacional=porc_nacional.comision_porcentaje/100
        porc_importado=porc_importado.comision_porcentaje/100

        facturas = self.env['account.invoice'].search(domain)
        for f in facturas:
            for fl in f.invoice_line_ids:
                if fl.product_id.product_tmpl_id.producto_origen=='nacional':
                    if fl.invoice_id.sii_code==61:
                        comision+=round(fl.price_subtotal*porc_nacional)*-1
                    else:
                        comision+=round(fl.price_subtotal*porc_nacional)
                else:
                    if fl.invoice_id.sii_code==61:
                        comision+=round(fl.price_subtotal*porc_importado)*-1
                    else:
                        comision+=round(fl.price_subtotal*porc_importado)
        payslip = self.env['hr.payslip.input'].search([('code', '=', 'COMI'),('contract_id','=',contrato_id.id),('payslip_id','=',self.id)])
        payslip.write({'amount': comision})
        return super(Nomina, self).compute_sheet()

    @api.model
    def get_created_after_date(self,fecha_actual,days):
        created_after = (fecha_actual - timedelta(days=days)).isoformat()
        return created_after