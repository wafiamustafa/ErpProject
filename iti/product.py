from openerp.osv import orm, fields

# class iti_product(orm.Model):
#     _name = 'iti.product'
#
#     def _calc_code(self, cr, uid, ids, name, arg, context=None):
#         result = {}
#         ids = self.search(cr, uid, [])
#         products = self.browse(cr, uid, ids, context)
#         for product in products:
#             #if (product.catagory_id and product.subcatagory_id and product.subsubcatagory_id):
#             result[product.id] = str(product.code) + " " + str(product.catagory_id.cat_id) + " " + str( product.subcatagory_id.subcat_id) + " " + str(product.subsubcatagory_id.subsubcat_id)
#
#         return result
#
#     def set_accepted(self, cr, uid, ids, context=None): pass
#
#     _columns = { 'name': fields.char('Name'), 'price': fields.float('Price'), 'support': fields.char('Support'), 'amount': fields.integer('Amount'), 'productdate': fields.date('Productdate'), 'expirdate': fields.date('Expirdate'), 'code': fields.integer('Code', size=2, required=True), 'net_code': fields.function(_calc_code, string='Reference', method=True, type='char', store=True), 'desc': fields.text('description'), 'catagory_id': fields.many2one('iti.catagory', string='catagory'), 'subcatagory_id': fields.many2one('iti.subcatagory', string='subcatagory'), 'subsubcatagory_id': fields.many2one('iti.subsubcatagory', string='subsubcatagory'), 'state': fields.selection(string="State", default='new', selection=[ ('new', 'New'), ('recieved', 'Recieved'), ('underReview', 'Under Review'), ('approved', 'Approved'), ('keeperConfirm', 'Keeper Confirm'), ('managerConfirm', 'Manager Confirm'), ('inStock', 'In Stock'), ], readonly=True), 'warehouse_id': fields.many2one("iti.warehouse", "Warehouse"), }
#
#     ###### functions#######
#
#     def product_new(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'new'})
#         return True
#
#     def product_recieved(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'recieved'})
#         return True
#
#     def product_underReview(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'underReview'})
#         return True
#
#     def product_approved(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'approved'})
#         return True
#
#     def product_keeper_confirm(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'keeperConfirm'})
#         return True
#
#     def product_manager_confirm(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'managerConfirm'})
#         return True
#
#     def product_in_stock(self, cr, uid, ids):
#         self.write(cr, uid, ids, {'state': 'inStock'})
#         return True

class iti_product(orm.Model):

    _name = 'iti.product'

    def fun(self, cr, uid, ids, context=None):
        pass

    def _product_code(self, cr, uid, ids, name, arg, context=None):
        result = {}
        all_ids = self.search(cr, uid, [])
        products = self.browse(cr, uid, all_ids, context)
        for product in products:
            result[product.id] =str(product.code) + "" + str(product.catagory_id.cat_id )+ "" +str(product.subcatagory_id.subcat_id) + "" +str(product.subsubcatagory_id.subsubcat_id)
        return result
    def check_keeper(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            keeper_id = product.store_id.keeper_id.id
            res[product.id] = (keeper_id == uid)
            return res

    def check_manager(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            manager_id = product.store_id.manager_id.id
            res[product.id] = (manager_id == uid)
            return res

    def check_supermanager(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            supermanager_id = product.store_id.supermanager_id.id
            res[product.id] = (supermanager_id == uid)
            return res

    def check_committeeManager(self, cr, uid, ids, field_name, arg, context):
        res = {}
        for product in self.browse(cr, uid, ids, context=context):
            committeeManager_id = product.store_id.committeeManager_id.id
            res[product.id] = (committeeManager_id == uid)
            return res


    _columns = {
        'name': fields.char('Name'),
        'price': fields.float('Price'),
        'sale_price' : fields.float(string='Sale Price'),
        'min_qty': fields.integer(string='Minimum Quantity'),
        'max_qty': fields.integer(string='Maximum Quantity'),
        'qty_available': fields.integer(string='Quantity'),
        'incoming_qty': fields.integer(string='Incoming',),
        'outgoing_qty': fields.integer( string='Outgoing'),
        'productdate': fields.date('Productdate'),
        'expirdate': fields.date('Expirdate'),
        # 'code': fields.char('Code'),
        'code':fields.integer("Code",required="1",size=2),
        'complete_code': fields.function(_product_code, type='char', string='Complete Code'),
        # 'net_code': fields.function(_calc_code, string='Reference', method=True),
        'desc': fields.text('description'),
        'catagory_id': fields.many2one('iti.catagory', string='catagory'),
        'subcatagory_id': fields.many2one('iti.subcatagory', string='subcatagory'),
        'subsubcatagory_id': fields.many2one('iti.subsubcatagory', string='subsubcatagory'),
        'active': fields.boolean('Active', help="If unchecked, it will allow you to hide the product without removing it."),
        'suppliers_ids': fields.many2many('iti.supplier',string="Suppliers"),
        'store_id': fields.many2one('iti.store',string='Store'),
                'status':fields.selection(string="Status",selection=[
            ("new","New"),
            ('used',"Used"),
            ('damaged','Damaged'),
        ]),
        'state': fields.selection(string="State", default='new', selection=[ ('new', 'New'), ('recieved', 'Recieved'), ('underReview', 'Under Review'), ('approved', 'Approved'), ('keeperConfirm', 'Keeper Confirm'), ('managerConfirm', 'Manager Confirm'), ('inStock', 'In Stock') ], readonly=True),
        'is_keeper': fields.function(check_keeper, type='boolean', store=False),
        'is_manager': fields.function(check_manager, type='boolean', store=False),
        'is_supermanager': fields.function(check_supermanager, type='boolean', store=False),
        'is_committeeManager': fields.function(check_committeeManager, type='boolean', store=False),

        # 'state': fields.selection([('new', 'New'),
        #                            ('waitKeeperConfirmation', 'Wait Keeper Confirmation'),
        #                            ('waitManagerConfirmation', 'Wait Manager Confirmation'),
        #                            ('waitExamination', 'Wait Examination'),
        #                            ('inExamination', 'In Examination'),
        #                            ('examined', 'Exmined'),
        #                            ('excepted', 'excepted'),
        #                            ('rejected', 'Rejected'),], 'Status', readonly=True, select=True),
                 # ,help= "* New: When the stock move is created and not yet confirmed.\n"\
                 #       "* Waiting Another Move: This state can be seen when a move is waiting for another one, for example in a chained flow.\n"\
                 #       "* Waiting Availability: This state is reached when the procurement resolution is not straight forward. It may need the scheduler to run, a component to me manufactured...\n"\
                 #       "* Available: When products are reserved, it is set to \'Available\'.\n"\
                 #       "* Done: When the shipment is processed, the state is \'Done\'."),




        # 'color': fields.integer('Color Index'),
        # # image: all image fields are base64 encoded and PIL-supported
        # 'image': fields.binary("Image",
        #     help="This field holds the image used as image for the product, limited to 1024x1024px."),
        # 'image_medium': fields.function(_get_image, fnct_inv=_set_image,
        #     string="Medium-sized image", type="binary", multi="_get_image",
        #     store={
        #         'product.product': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        #     },
        #     help="Medium-sized image of the product. It is automatically "\
        #          "resized as a 128x128px image, with aspect ratio preserved, "\
        #          "only when the image exceeds one of those sizes. Use this field in form views or some kanban views."),
        # 'image_small': fields.function(_get_image, fnct_inv=_set_image,
        #     string="Small-sized image", type="binary", multi="_get_image",
        #     store={
        #         'product.product': (lambda self, cr, uid, ids, c={}: ids, ['image'], 10),
        #     },
        #     help="Small-sized image of the product. It is automatically "\
        #          "resized as a 64x64px image, with aspect ratio preserved. "\
        #          "Use this field anywhere a small image is required."),
    }
    _defaults = {
        'active':1,
        # 'state':'waitKeeperConfirmation',
        # 'sequence': lambda *a: 1,
        # 'delay': lambda *a: 1,
        # 'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'product.supplierinfo', context=c),
    }

    def action_formTeam(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'waitManagerConfirmation'})
        return True

    def action_waitExamine(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'waitExamination'})
        return True

    def action_examine(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'inExamination'})
        return True

    def action_showExaminationResult(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'examined'})
        return True
    def action_except(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'excepted'})
        return True
    def action_reject(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'rejected'})
        return True

    def product_new(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'new'})
        return True

    def product_recieved(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'recieved'})
        return True

    def product_underReview(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'underReview'})
        return True

    def product_approved(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'approved'})
        return True

    def product_keeper_confirm(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'keeperConfirm'})
        return True

    def product_manager_confirm(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'managerConfirm'})
        return True

    def product_in_stock(self, cr, uid, ids):
        self.write(cr, uid, ids, {'state': 'inStock'})
        return True
