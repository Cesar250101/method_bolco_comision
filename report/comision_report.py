# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools


class ComisionesReport(models.Model):
    _name = 'method_bolco_comision.comision_report'
    _description = "Respote de comisiones"
    _auto = False
    _order = 'date_invoice'

    date_invoice = fields.Date(string='Fecha',readonly=True,)
    number = fields.Char(string='Nro',readonly=True,)
    sii_document_number = fields.Integer(string='Nro Docto',readonly=True,)
    document_number = fields.Integer(string="Rut",readonly=True,)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')    
    product_id = fields.Many2one('product.product',string='Producto',readonly=True,)
    product_tmpl_id= fields.Many2one('product.template',string='Plantilla Producto',readonly=True,)
    quantity = fields.Integer(string='Cantidad')    
    producto_origen = fields.Char(string='Origen Producto')    
    price_subtotal = fields.Integer(string='Neto',readonly=True,)
    user_id=fields.Many2one('res.user',string="Usuario")



    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (select 
            ROW_NUMBER() OVER() AS id,ai.date_invoice ,ai.number,ai.sii_document_number,rp.document_number ,
            rp.id as partner_id,pp.id as product_id,pt.id as product_tmpl_id,
                    ail.quantity,pt.producto_origen ,ail.price_subtotal,ru.id as user_id
                    from account_invoice ai ,
                    account_invoice_line ail ,product_product pp ,product_template pt ,res_users ru,
                    res_partner rp, res_partner rp2  
                    where ai.id=ail.invoice_id 
                    and ail.product_id =pp.id 
                    and pp.product_tmpl_id =pt.id 
                    and ai.user_id =ru.id 
                    and ai.partner_id =rp.id 
                    and ru.partner_id =rp2.id                
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))
