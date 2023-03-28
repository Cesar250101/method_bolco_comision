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
    product_id = fields.Many2one(comodel_name='product.product',string='Producto',readonly=True,)
    product_tmpl_id= fields.Many2one(comodel_name='product.template',string='Plantilla Producto',readonly=True,)
    quantity = fields.Integer(string='Cantidad')    
    producto_origen = fields.Char(string='Origen Producto')    
    price_subtotal = fields.Integer(string='Neto',readonly=True,)
    vendedor = fields.Char(string='Vendedor')
    tipo_documento = fields.Char(string='Tipo Documento')
    pago = fields.Char(string='Pago')



    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (select 
                ROW_NUMBER() OVER() AS id,
                ap.payment_date  as date_invoice ,
                ai.number as number,
                ai.sii_document_number as sii_document_number,
                rp.document_number as document_number,
                rp.id as partner_id,
                pp.id as product_id,
                pt.id as product_tmpl_id,
                ail.quantity as quantity,
                pt.producto_origen as producto_origen ,
                case when ai.sii_code =61 then ail.price_subtotal*-1 else ail.price_subtotal end  as price_subtotal,
                rp2.name as vendedor,sdc.name as tipo_documento,
                ap.name as pago
                from account_invoice ai ,account_invoice_line ail,product_product pp,product_template pt,res_users ru,
                res_partner rp,res_partner rp2,sii_document_class sdc,account_invoice_payment_rel aipr,account_payment ap  
                where ai.id=ail.invoice_id 
                and ai.id=aipr.invoice_id 
                and aipr.payment_id =ap.id 
                and ail.product_id =pp.id 
                and pp.product_tmpl_id =pt.id 
                and ai.user_id =ru.id 
                and ai.partner_id =rp.id 
                and ru.partner_id =rp2.id 
                and ai.document_class_id =sdc.id
                and ai.sii_code in('33','34','56','39','61')     
                union
                select ROW_NUMBER() OVER() AS id,
                ai.date_invoice  as date_invoice ,
                ai.number as number,
                ai.sii_document_number as sii_document_number,
                rp.document_number as document_number,
                rp.id as partner_id,
                pp.id as product_id,
                pt.id as product_tmpl_id,
                ail.quantity as quantity,
                pt.producto_origen as producto_origen ,
                case when ai.sii_code =61 then ail.price_subtotal*-1 else ail.price_subtotal end  as price_subtotal,
                rp2.name as vendedor,sdc.name as tipo_documento,
                'SinPago' as pago
                from account_invoice ai ,account_invoice_line ail,product_product pp,product_template pt,res_users ru,
                res_partner rp,res_partner rp2,sii_document_class sdc  
                where ai.id=ail.invoice_id 
                and ail.product_id =pp.id 
                and pp.product_tmpl_id =pt.id 
                and ai.user_id =ru.id 
                and ai.partner_id =rp.id 
                and ru.partner_id =rp2.id 
                and ai.document_class_id =sdc.id
                and ai.sii_code in('56','61')
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))

class ComisionesReport(models.Model):
    _name = 'method_bolco_comision.comision_report_sin_pago'
    _description = "Respote de comisiones - Factura emitida (No se condideran los pagos)"
    _auto = False
    _order = 'date_invoice'

    date_invoice = fields.Date(string='Fecha',readonly=True,)
    number = fields.Char(string='Nro',readonly=True,)
    sii_document_number = fields.Integer(string='Nro Docto',readonly=True,)
    document_number = fields.Integer(string="Rut",readonly=True,)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')    
    product_id = fields.Many2one(comodel_name='product.product',string='Producto',readonly=True,)
    product_tmpl_id= fields.Many2one(comodel_name='product.template',string='Plantilla Producto',readonly=True,)
    quantity = fields.Integer(string='Cantidad')    
    producto_origen = fields.Char(string='Origen Producto')    
    price_subtotal = fields.Integer(string='Neto',readonly=True,)
    vendedor = fields.Char(string='Vendedor')
    tipo_documento = fields.Char(string='Tipo Documento')
    journal_id = fields.Many2one(comodel_name='comodel_name', string='Diario')


    @api.model_cr
    def init(self):
        user=self.env.uid
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE OR REPLACE VIEW %s AS (select 
                ROW_NUMBER() OVER() AS id,
                ai.date_invoice  as date_invoice ,
                ai.number as number,
                ai.sii_document_number as sii_document_number,
                rp.document_number as document_number,
                rp.id as partner_id,
                pp.id as product_id,
                pt.id as product_tmpl_id,
                ail.quantity as quantity,
                pt.producto_origen as producto_origen ,
                case when ai.sii_code =61 then ail.price_subtotal*-1 else ail.price_subtotal end  as price_subtotal,
                rp2.name as vendedor,sdc.name as tipo_documento,aj.id journal_id 
                from account_invoice ai ,account_invoice_line ail,product_product pp,product_template pt,res_users ru,
                res_partner rp,res_partner rp2,sii_document_class sdc,account_journal aj 
                where ai.id=ail.invoice_id 
                and ai.journal_id =aj.id 
                and ail.product_id =pp.id 
                and pp.product_tmpl_id =pt.id 
                and ai.user_id =ru.id 
                and ai.partner_id =rp.id 
                and ru.partner_id =rp2.id 
                and ai.document_class_id =sdc.id
                and ai.sii_code in('33','34','56','39','61')   
                and aj.type='sale'
                union
                select ROW_NUMBER() OVER() AS id,
                ai.date_invoice  as date_invoice ,
                ai.number as number,
                ai.sii_document_number as sii_document_number,
                rp.document_number as document_number,
                rp.id as partner_id,
                pp.id as product_id,
                pt.id as product_tmpl_id,
                ail.quantity as quantity,
                pt.producto_origen as producto_origen ,
                case when ai.sii_code =61 then ail.price_subtotal*-1 else ail.price_subtotal end  as price_subtotal,
                rp2.name as vendedor,sdc.name as tipo_documento,aj2.id journal_id 
                from account_invoice ai ,account_invoice_line ail,product_product pp,product_template pt,res_users ru,
                res_partner rp,res_partner rp2,sii_document_class sdc,account_journal aj2  
                where ai.id=ail.invoice_id 
                and ail.product_id =pp.id 
                and pp.product_tmpl_id =pt.id 
                and ai.user_id =ru.id 
                and ai.partner_id =rp.id 
                and ru.partner_id =rp2.id 
                and ai.document_class_id =sdc.id
                and ai.sii_code in('56','61')
                and aj2.type='sale'                
            )
        """ % (
            self._table
            #self._select(), self._from(),user, self._group_by(), self._having(),

        ))
