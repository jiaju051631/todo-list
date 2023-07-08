from pathlib import Path
import pytest
import sys

top_level_dir = Path(__file__).parent.parent
sys.path.insert(0, str(top_level_dir))

from app import create_test_app, db
from models import User, OAuth, Task
import config

TEST_ACCESS_TOKEN = config.VALID_ACCESS_TOKEN


# Create the app and database for testing
@pytest.fixture(scope="session")
def app():
    return create_test_app()


# Create a test client
@pytest.fixture(scope="session")
def client(app):
    return app.test_client()


# Delete and insert test data for User, OAuth and Task
# in the test database
@pytest.fixture(autouse=True, scope="session")
def setup(app):
    with app.app_context():
        User.query.delete()
        OAuth.query.delete()
        Task.query.delete()
    
        test_user = User(username=config.TEST_USER_NAME)

        test_oauth = OAuth(
            user=test_user,
            provider=config.TEST_OAUTH_PROVIDER,
            provider_user_id=config.TEST_OAUTH_PROVIDER_USER_ID,
            token={"access_token": config.VALID_ACCESS_TOKEN}
        )

        db.session.add_all([test_user, test_oauth])
        db.session.commit()


# Insert a new Task into the test database,
# and delete the task after the test case is executed
@pytest.fixture(scope="function")
def add_and_delete_task(app, request):
    with app.app_context():

        test_user = User.query.filter_by(
            username=config.TEST_USER_NAME
        ).first()

        test_task = Task(
            user=test_user,
            task_name=config.TEST_TASK_NAME
        )
        db.session.add(test_task)
        db.session.commit()
        
        def teardown():
            with app.app_context():
                Task.query.delete()
                db.session.commit()

        # Add the finalizer to delete the Task record
        request.addfinalizer(teardown)


