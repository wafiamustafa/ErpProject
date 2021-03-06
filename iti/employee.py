from openerp import addons
import logging
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import tools

class iti_employee(osv.osv):
    _name = "iti.employee"
    _description = "Employee"
    _inherits = {'resource.resource': "resource_id"}

    def _get_image(self, cr, uid, ids, name, args, context=None):
        result = dict.fromkeys(ids, False)
        for obj in self.browse(cr, uid, ids, context=context):
            result[obj.id] = tools.image_get_resized_images(obj.image)
        return result
    
    def _set_image(self, cr, uid, id, name, value, args, context=None):
        return self.write(cr, uid, [id], {'image': tools.image_resize_image_big(value)}, context=context)
    
    _columns = {
        #we need a related field in order to be able to sort the employee by name
        'name_related': fields.related('resource_id', 'name', type='char', string='Name', readonly=True, store=True),
        # 'country_id': fields.many2one('res.country', 'Nationality'),
        'birthday': fields.date("Date of Birth"),
        'ssnid': fields.char('SSN No', size=32, help='Social Security Number'),
        # 'sinid': fields.char('SIN No', size=32, help="Social Insurance Number"),
        'identification_id': fields.char('Identification No', size=32),
        # 'otherid': fields.char('Other Id', size=64),
        'gender': fields.selection([('male', 'Male'),('female', 'Female')], 'Gender'),
        'marital': fields.selection([('single', 'Single'), ('married', 'Married'), ('widower', 'Widower'), ('divorced', 'Divorced')], 'Marital Status'),
        # 'department_id':fields.many2one('hr.department', 'Department'),
        # 'address_id': fields.many2one('res.partner', 'Working Address'),
        'address': fields.char('Address',size=100, help='Complete Address.'),
        # 'address_home_id': fields.many2one('res.partner', 'Home Address'),
        # 'bank_account_id':fields.many2one('res.partner.bank', 'Bank Account Number', domain="[('partner_id','=',address_home_id)]", help="Employee bank salary account"),
        'work_phone': fields.char('Work Phone', size=32, readonly=False),
        'mobile_phone': fields.char('Work Mobile', size=32, readonly=False),
        'work_email': fields.char('Work Email', size=240),
        # 'work_location': fields.char('Office Location', size=32),
        # 'notes': fields.text('Notes'),
        'parent_id': fields.many2one('iti.employee', 'Manager'),
        # 'category_ids': fields.many2many('hr.employee.category', 'employee_category_rel', 'emp_id', 'category_id', 'Tags'),
        'child_ids': fields.one2many('iti.employee', 'parent_id', 'Subordinates'),
        'resource_id': fields.many2one('resource.resource', 'Resource', ondelete='cascade', required=True),
        # 'coach_id': fields.many2one('hr.employee', 'Coach'),
        'job_id': fields.many2one('iti.job', 'Job'),
        'store_id': fields.many2one('iti.store', 'Store'),
        # image: all image fields are base64 encoded and PIL-supported
        # 'image': fields.binary("Photo",
        #     help="This field holds the image used as photo for the employee, limited to 1024x1024px."),
        # 'image_medium': fields.function(_get_image, fnct_inv=_set_image,
        #     string="Medium-sized photo", type="binary", multi="_get_image",
        #     store = {
        #         'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        #     },
        #     help="Medium-sized photo of the employee. It is automatically "\
        #          "resized as a 128x128px image, with aspect ratio preserved. "\
        #          "Use this field in form views or some kanban views."),
        # 'image_small': fields.function(_get_image, fnct_inv=_set_image,
        #     string="Small-sized photo", type="binary", multi="_get_image",
        #     store = {
        #         'hr.employee': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        #     },
        #     help="Small-sized photo of the employee. It is automatically "\
        #          "resized as a 64x64px image, with aspect ratio preserved. "\
        #          "Use this field anywhere a small image is required."),
        # 'passport_id':fields.char('Passport No', size=64),
        # 'color': fields.integer('Color Index'),
        # 'city': fields.related('address_id', 'city', type='char', string='City'),
        # 'login': fields.related('user_id', 'login', type='char', string='Login', readonly=1),
        # 'last_login': fields.related('user_id', 'date', type='datetime', string='Latest Connection', readonly=1),
    }

    _order='name_related'
    
    def copy_data(self, cr, uid, ids, default=None, context=None):
        if default is None:
            default = {}
        default.update({'child_ids': False})
        return super(iti_employee, self).copy_data(cr, uid, ids, default, context=context)
        
    def create(self, cr, uid, data, context=None):
        employee_id = super(iti_employee, self).create(cr, uid, data, context=context)
        try:
            (model, mail_group_id) = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'mail', 'group_all_employees')
            employee = self.browse(cr, uid, employee_id, context=context)
            self.pool.get('mail.group').message_post(cr, uid, [mail_group_id],
                body=_('Welcome to %s! Please help him/her take the first steps with OpenERP!') % (employee.name),
                subtype='mail.mt_comment', context=context)
        except:
            pass # group deleted: do not push a message
        return employee_id

    def unlink(self, cr, uid, ids, context=None):
        resource_ids = []
        for employee in self.browse(cr, uid, ids, context=context):
            resource_ids.append(employee.resource_id.id)
        super(iti_employee, self).unlink(cr, uid, ids, context=context)
        return self.pool.get('resource.resource').unlink(cr, uid, resource_ids, context=context)

    def onchange_address_id(self, cr, uid, ids, address, context=None):
        if address:
            address = self.pool.get('res.partner').browse(cr, uid, address, context=context)
            return {'value': {'work_phone': address.phone, 'mobile_phone': address.mobile}}
        return {'value': {}}

    def onchange_company(self, cr, uid, ids, company, context=None):
        address_id = False
        if company:
            company_id = self.pool.get('res.company').browse(cr, uid, company, context=context)
            address = self.pool.get('res.partner').address_get(cr, uid, [company_id.partner_id.id], ['default'])
            address_id = address and address['default'] or False
        return {'value': {'address_id' : address_id}}

    # def onchange_department_id(self, cr, uid, ids, department_id, context=None):
    #     value = {'parent_id': False}
    #     if department_id:
    #         department = self.pool.get('hr.department').browse(cr, uid, department_id)
    #         value['parent_id'] = department.manager_id.id
    #     return {'value': value}

    def onchange_user(self, cr, uid, ids, user_id, context=None):
        work_email = False
        if user_id:
            work_email = self.pool.get('res.users').browse(cr, uid, user_id, context=context).email
        return {'value': {'work_email' : work_email}}

    # def _get_default_image(self, cr, uid, context=None):
    #     image_path = addons.get_module_resource('hr', 'static/src/img', 'default_image.png')
    #     return tools.image_resize_image_big(open(image_path, 'rb').read().encode('base64'))

    #
    # def _check_recursion(self, cr, uid, ids, context=None):
    #     level = 100
    #     while len(ids):
    #         cr.execute('SELECT DISTINCT parent_id FROM hr_employee WHERE id IN %s AND parent_id!=id',(tuple(ids),))
    #         ids = filter(None, map(lambda x:x[0], cr.fetchall()))
    #         if not level:
    #             return False
    #         level -= 1
    #     return True
    #
    # _constraints = [
    #     (_check_recursion, 'Error! You cannot create recursive hierarchy of Employee(s).', ['parent_id']),
    # ]

iti_employee()


# --------------------------------------------------------------------------------------

# class res_users(osv.osv):
#     _name = 'res.users'
#     _inherit = 'res.users'
#
#     def copy_data(self, cr, uid, ids, default=None, context=None):
#         if default is None:
#             default = {}
#         default.update({'employee_ids': False})
#         return super(res_users, self).copy_data(cr, uid, ids, default, context=context)
#
#     def create(self, cr, uid, data, context=None):
#         user_id = super(res_users, self).create(cr, uid, data, context=context)
#
#         # add shortcut unless 'noshortcut' is True in context
#         if not(context and context.get('noshortcut', False)):
#             data_obj = self.pool.get('ir.model.data')
#             try:
#                 data_id = data_obj._get_id(cr, uid, 'hr', 'ir_ui_view_sc_employee')
#                 view_id  = data_obj.browse(cr, uid, data_id, context=context).res_id
#                 self.pool.get('ir.ui.view_sc').copy(cr, uid, view_id, default = {
#                                             'user_id': user_id}, context=context)
#             except:
#                 # Tolerate a missing shortcut. See product/product.py for similar code.
#                 _logger.debug('Skipped meetings shortcut for user "%s".', data.get('name','<new'))
#
#         return user_id
#
#     _columns = {
#         'employee_ids': fields.one2many('iti.employee', 'user_id', 'Related employees'),
#         }
#
# res_users()

# ---------------------------------------------------------------------------------------------
class iti_job(osv.osv):

    def _no_of_employee(self, cr, uid, ids, name, args, context=None):
        res = {}
        for job in self.browse(cr, uid, ids, context=context):
            nb_employees = len(job.employee_ids or [])
            res[job.id] = {
                'no_of_employee': nb_employees,
                'expected_employees': nb_employees + job.no_of_recruitment,
            }
        return res

    def _get_job_position(self, cr, uid, ids, context=None):
        res = []
        for employee in self.pool.get('iti.employee').browse(cr, uid, ids, context=context):
            if employee.job_id:
                res.append(employee.job_id.id)
        return res

    _name = "iti.job"
    _description = "Job Description"
    _inherit = ['mail.thread']
    _columns = {
        'name': fields.char('Job Name', size=128, required=True, select=True),
        # 'expected_employees': fields.function(_no_of_employee, string='Total Forecasted Employees',
        #     help='Expected number of employees for this job position after new recruitment.',
        #     store = {
        #         'hr.job': (lambda self,cr,uid,ids,c=None: ids, ['no_of_recruitment'], 10),
        #         'hr.employee': (_get_job_position, ['job_id'], 10),
        #     },
        #     multi='no_of_employee'),
        # 'no_of_employee': fields.function(_no_of_employee, string="Current Number of Employees",
        #     help='Number of employees currently occupying this job position.',
        #     store = {
        #         'hr.employee': (_get_job_position, ['job_id'], 10),
        #     },
        #     multi='no_of_employee'),
        # 'no_of_recruitment': fields.float('Expected in Recruitment', help='Number of new employees you expect to recruit.'),
        'employee_ids': fields.one2many('iti.employee', 'job_id', 'Employees', groups='base.group_user'),
        'description': fields.text('Job Description'),
        'requirements': fields.text('Requirements'),
        # 'department_id': fields.many2one('hr.department', 'Department'),
        # 'company_id': fields.many2one('res.company', 'Company'),
        # 'state': fields.selection([('open', 'No Recruitment'), ('recruit', 'Recruitement in Progress')], 'Status', readonly=True, required=True,
        #     help="By default 'In position', set it to 'In Recruitment' if recruitment process is going on for this job position."),
    }
    # _defaults = {
    #     'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'hr.job', context=c),
    #     'state': 'open',
    # }

    # _sql_constraints = [
    #     ('name_company_uniq', 'unique(name, company_id)', 'The name of the job position must be unique per company!'),
    # ]
    _sql_constraints = [
        ('name_company_uniq', 'unique(name)', 'The name of the job position must be unique per company!'),
    ]


    def on_change_expected_employee(self, cr, uid, ids, no_of_recruitment, no_of_employee, context=None):
        if context is None:
            context = {}
        return {'value': {'expected_employees': no_of_recruitment + no_of_employee}}

    def job_recruitement(self, cr, uid, ids, *args):
        for job in self.browse(cr, uid, ids):
            no_of_recruitment = job.no_of_recruitment == 0 and 1 or job.no_of_recruitment
            self.write(cr, uid, [job.id], {'state': 'recruit', 'no_of_recruitment': no_of_recruitment})
        return True

    def job_open(self, cr, uid, ids, *args):
        self.write(cr, uid, ids, {'state': 'open', 'no_of_recruitment': 0})
        return True

iti_job()
