from app import app, db
from sqlalchemy.ext.automap import automap_base

# generate model classes based on the already created
# database (the engine is the postgres connection)
Base = automap_base()
Base.prepare(db.engine, reflect=True)

# get the model from the mapped database
RadAcct = Base.classes.radacct
RadCheck = Base.classes.radcheck
RadGroupCheck = Base.classes.radgroupcheck
RadGroupReply = Base.classes.radgroupreply
RadReply = Base.classes.radreply
RadUserGroup = Base.classes.radusergroup
RadPostAuth = Base.classes.radpostauth
Nas = Base.classes.nas