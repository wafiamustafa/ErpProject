from openerp.osv import orm, fields
class iti_search(orm.Model):
    _name = 'iti.search'

    ch = [('name', 'Name'), ('complete_code', 'Code')]
    _columns = {
        'search': fields.char(string='Search', size=100),
        'change': fields.selection(ch, string='Search By', size=100),
        'result': fields.text(string='Results', size=500)}


    def func1(self, cr, uid, ids, search, change, context=None):

        record = self.pool.get('iti.product').search(cr, uid, [(change, '=', search)])
        record = self.pool.get('iti.product').read(cr, uid, record)
        if record:
            v = {'result': 'Name:' + str(record[0]['name']) + ',Status:' + str(record[0]['status'])
                           + ',Code:' + str(record[0]['complete_code'])
                           + ',Quantity:' + str(record[0]['qty_available']) + ',Price:' + str(record[0]['price'])
                           + ',Description:' + str(record[0]['desc'])}

        else:
            v = {'result': ''}
        return {'value': v}

