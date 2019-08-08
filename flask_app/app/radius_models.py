from app import db
from sqlalchemy.ext.automap import automap_base

Base = automap_base()
Base.prepare(db.engine, reflect=True)

RadAcct = Base.classes.radacct
RadCheck = Base.classes.radcheck
RadGroupCheck = Base.classes.radgroupcheck
RadGroupReply = Base.classes.radgroupreply
RadReply = Base.classes.radreply
RadUserGroup = Base.classes.radusergroup
RadPostAuth = Base.classes.radpostauth
Nas = Base.classes.nas