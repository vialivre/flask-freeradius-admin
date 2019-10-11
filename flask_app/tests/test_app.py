import os
import tempfile

import pytest

from app import app

@pytest.fixture
def client():
    db_fd, db_name = tempfile.mkstemp()
    print(db_fd)
    print(db_name)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['SQLALCHEMY_DATABASE_URI'])