from openerp.osv import orm, fields


class iti_catagory(orm.Model):
    _name = 'iti.catagory'
    _columns = {
        'name': fields.char('Name'),
        'cat_id':fields.char("Code",required="1",size=2),
        'desc': fields.text('description'),
    }


class iti_subcatagory(orm.Model):
    _name = 'iti.subcatagory'
    _columns = {
        'name': fields.char('Name'),
        'subcat_id':fields.char("Code",required="1",size=2),
        'desc': fields.text('description'),
        'catagory_id': fields.many2one('iti.catagory', string='catagory'),
    }


class iti_subsubcatagory(orm.Model):
    _name = 'iti.subsubcatagory'
    _columns = {
        'name': fields.char('Name'),
        'subsubcat_id': fields.char("Code",required="1",size=2),
        'desc': fields.text('description'),
        'subcatagory_id': fields.many2one('iti.subcatagory', string='subcatagory'),
    }


