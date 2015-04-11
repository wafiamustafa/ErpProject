from openerp.osv import orm,fields

class iti_students(orm.Model):
    _name="iti.student"
    _columns = {
        "name":fields.char("name"),
        "age":fields.integer("age"),
        "salary":fields.float("salary"),
        "faculty":fields.char("faculty"),
        "grade":fields.selection([("g","good"),("v","verygood"),("e","exelent")],"faculty"),
        "graduation_year":fields.selection([("2013","2013"),("2014","2014")],"graduation_year"),
        "comment":fields.html("comment"),
        "request":fields.char("request"),
        "accepted":fields.boolean("accepted"),
        "image":fields.binary("image"),
        "dept_id":fields.many2one("iti.department","department"),
        "skill_id":fields.many2many("iti.skill","skills")
        }
    def change_dept(self, cr, uid, ids,skill_id, context=None):
        values={}
        skill_ids=skill_id[0][2]
        skills = self.pool.get('iti.skill').browse(cr, uid,skill_ids)

        for skill in skills:
            d_id=skill.dept_id.id
            if skill.dept_id.id !=d_id:
                return  {'value' :{"dept_id":"mix"}}
        x=self.pool.get('iti.department').browse(cr, uid,skills[0].dept_id.id)
        dep_name=self.pool.get('iti.department').browse(cr, uid,skills[0].dept_id.id).name
        return  {'value' :{"dept_id":dep_name}}




class iti_departments(orm.Model):
    _name="iti.department"
    _columns = {
        "name":fields.char("name"),
        "desc":fields.text("description"),
        "skill_ids":fields.many2many("iti.skill","skills")

        }

class iti_skills(orm.Model):
    _name="iti.skill"
    _columns = {
        "name":fields.char("name"),
        "desc":fields.text("description"),
        "dept_id":fields.many2many("iti.department", "skills")

        }