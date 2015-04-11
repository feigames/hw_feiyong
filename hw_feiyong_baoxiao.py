import openerp.addons.decimal_precision as dp
from openerp import models,fields,api,exceptions, _
import time

class hw_feiyong_baoxiao(models.Model):
    _name='hw.feiyong.baoxiao'
    
    _inherit ='mail.thread'

    _description='hw.feiyong.baoxiao'

    name=fields.Char(default=lambda self:self.env['ir.sequence'].get('hw.feiyong.baoxiao') or '/',
        copy=False,readonly=True)

    state=fields.Selection([('draft','Draft'),
        ('manager','Manager'),
        ('fr','Reviewed by Accountant'),
        ('dgm','Deputy General Manager'),
        ('gm','General Manager'),
        ('approved','Approved'),
        ('refused','Refused'),
        ('paid','Paid')],'status',copy=False,readonly=True,track_visibility='onchange',default='draft')

    payment=fields.Selection([('cash','Cash'),('bt','Bank Transfer'),
        ('oca','Offset Cash Advance'),('other','Other')],'Payment',copy=False,
        states={'draft':[('readonly',False)]},readonly=True,default='cash',required=True)

    date_invoice=fields.Date(default=fields.Date.today,required=True,copy=False,select=True,
        states={'draft':[('readonly',False)]},readonly=True)

    description=fields.Char(required=True,copy=True,select=True,
        states={'draft':[('readonly',False)]},readonly=True)

    note=fields.Text('note',states={'draft':[('readonly',False)]})

    date_paid=fields.Date('payment day',copy=False,readonly=True,select=True)

    employee_id=fields.Many2one('res.users','Employee',required=True,readonly=True,copy=False,
        default=lambda self:self.env.user)

    cashier_id=fields.Many2one('res.users','Cashier',readonly=True,copy=False)

    department_id=fields.Many2one('hr.department','Department',required=True,readonly=True,copy=False,
        default=lambda self:self.env.user.department_id)

    company_id=fields.Many2one('res.company','Company',required=True,readonly=True,copy=False,
        default=lambda self:self.env.user.company_id)

    company_lz=fields.Many2one('res.company','Building Company',required=True,copy=False,
        default=lambda self:self.env.user.company_id,states={'draft':[('readonly',False)]},readonly=True)

    job_id=fields.Many2one('hr.job','Job',required=True,readonly=True,copy=False,
        default=lambda self:self.env.user.job_id)

    line_ids=fields.One2many('hw.feiyong.baoxiao.lines','baoxiao_id','Expense Lines',copy=True,
        readonly=True,states={'draft':[('readonly',False)]})

    amount=fields.Float(compute='_amount',string='Amount',method=True,select=True,store=True,readonly=True,
        digits_compute=dp.get_precision('Account'))

    currency=fields.Many2one('res.currency','Currency',required=True,copy=False,select=True,
        states={'draft':[('readonly',False)]},readonly=True,default=lambda self:self.env.user.company_id.currency_id)

    rate=fields.Float(compute='_rate',store=True,string='Rate',readonly=True)

    st_amount=fields.Float(compute='_st_amount',string='ST_Amount',method=True,select=True,store=True,readonly=True,
        digits_compute=dp.get_precision('Account'))

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The NO. must be unique !'),
    ]

    @api.one
    def unlink(self):
        if self.state != 'draft':
            raise exceptions.ValidationError(_('You can only delete the state of the draft documents!'))
        super(hw_feiyong_baoxiao,self).unlink()

    @api.one
    @api.constrains('line_ids')
    def _check_lines(self):
        if not self.line_ids:
            raise exceptions.ValidationError(_("Not Expense lines"))



    @api.one
    @api.depends('line_ids')
    def _amount(self):
        #total=0.0
        for line in self.line_ids:
            self.amount+=line.jine
        return self.amount

    @api.one
    @api.depends('amount','rate')
    def _st_amount(self):
        self.st_amount=self.amount/self.rate
        return self.st_amount

    @api.one
    @api.onchange('currency')
    def _conchange_currency(self):
        if self.currency:
            self.rate=self.currency.rate_silent

    @api.one
    @api.depends('currency')
    def _rate(self):
        if self.currency:
            self.rate=self.currency.rate_silent
        return self.rate

    @api.one
    def baoxiao_fukuan(self):
        self.state='paid'
        self.date_paid=time.strftime('%Y-%m-%d')
        self.cashier_id=self.env.user


class hw_feiyong_baoxiao_lines(models.Model):
    _name='hw.feiyong.baoxiao.lines'

    _description='hw.feiyong.baoxiao.lines'

    baoxiao_id=fields.Many2one('hw.feiyong.baoxiao','baoxiao_id',ondelete='cascade',select=True)
    jine=fields.Float('money')
    note=fields.Text('Notes')
    account=fields.Many2one('account.account','Account',domain=[('type','!=','view')])
