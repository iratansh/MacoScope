class AuthRouter:
    """
    A router to control all database operations on models in the
    authentication application.
    """

    def db_for_read(self, model, **hints):
        """
        Attempts to read authentication models go to authentication.
        """
        if model._meta.app_label == 'authentication':
            return 'authentication'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write authentication models go to authentication.
        """
        if model._meta.app_label == 'authentication':
            return 'authentication'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the authentication app is involved.
        """
        if obj1._meta.app_label == 'authentication' or \
           obj2._meta.app_label == 'authentication':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure that authentication models get created on the right database.
        """
        if app_label == 'authentication':
            return db == 'authentication'
        return None


