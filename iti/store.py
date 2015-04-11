from openerp.osv import orm, fields

class iti_supplier(orm.Model):
    _name = "iti.supplier"
    _columns = {
        'name' : fields.char('Supplier Name', required=True),
        'mail' : fields.char('Supplier E_mail'),
        'mobile' : fields.char('Supplier Mobile'),
        'address' : fields.char('Supplier Address'),
        'products_ids': fields.many2many('iti.product','products_suppliers',string='products'),
        }




class iti_store(orm.Model):
    _name = "iti.store"
    _columns = {
        'name' : fields.char('Store Name', required=True),
        'location' : fields.char('Store Location', required=True),
        'products_ids' : fields.many2many('iti.product',string='Products'),
        'employees_ids' : fields.one2many('iti.employee','store_id',string='Employees'),
        'keeper_id': fields.many2one('res.users', "Keeper"),
        'manager_id': fields.many2one('res.users', "Manager"),
        'supermanager_id': fields.many2one('res.users', "Super Manager"),#, domain="[('id','=','ref('iti.iti_supermanager')')]"
        'committeeManager_id': fields.many2one('res.users', "Committee Manager"),

        }

class iti_commitee(orm.Model):
    _name = "iti.commitee"
    _columns = {
        'employees_ids' : fields.many2many('iti.employee',string='Employees'),
        'product_id' : fields.many2one('iti.product',string='Product'),

    }