class QuizRouter:
    """
    A router to control all database operations on models in the
    classroom application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read classroom models go to quiz_db.
        """
        if model._meta.app_label == 'classroom':
            return 'quiz'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write classroom models go to quiz_db.
        """
        if model._meta.app_label == 'classroom':
            return 'quiz'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the classroom app is involved.
        """
        if obj1._meta.app_label == 'classroom' or \
           obj2._meta.app_label == 'classroom':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label == 'classroom':
            return db == 'quiz'
        return None
