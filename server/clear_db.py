from app import app
import models as m

if __name__ == '__main__':
    with app.app_context():
        # Clear all tables

        # Reverse iterating through sorted_tables ensures there are no 
        # foreign keys referencing a table by the time we try to delete it.
        for table in reversed(m.db.metadata.sorted_tables):
            m.db.session.execute(table.delete())
        m.db.session.commit()
