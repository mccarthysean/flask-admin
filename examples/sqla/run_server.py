import sys
import pathlib
import os
import os.path as op

# Insert the python path into the front of the PATH environment variable, before importing any of my Python modules
pythonpath = str(pathlib.Path(__file__).parent)
try:
    sys.path.index(str(pythonpath))
except ValueError:
    sys.path.insert(0, str(pythonpath))

from admin import app
from admin.data import build_sample_db

# Build a sample db on the fly, if one does not exist yet.
app_dir = op.join(op.realpath(os.path.dirname(__file__)), 'admin')
database_path = op.join(app_dir, app.config['DATABASE_FILE'])
if not os.path.exists(database_path):
    build_sample_db()

if __name__ == '__main__':
    # Start app
    app.run(debug=True)
