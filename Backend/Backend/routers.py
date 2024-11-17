class AuthenticationRouter:
    """
    A router to control all database operations on models in the auth and contenttypes apps.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to authentication db.
        """
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions']:
            return 'authentication'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to authentication db.
        """
        if model._meta.app_label in ['auth', 'contenttypes', 'sessions']:
            return 'authentication'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is involved.
        """
        
        if obj1._meta.app_label in ['auth', 'contenttypes', 'sessions'] or obj2._meta.app_label in ['auth', 'contenttypes', 'sessions']:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Determine if the migration operation is allowed to run on the specified database.
        This method ensures that migrations for the 'auth', 'contenttypes', 
        and 'sessions' apps are only allowed on the 'authentication' database.

        Args:
            db (str): The name of the database.
            app_label (str): The label of the application.
            model_name (str, optional): The name of the model.
            **hints: Additional hints or context.

        Returns:
            bool or None: Returns True if the operation is allowed, otherwise None.
        """
        if app_label in ['auth', 'contenttypes', 'sessions']:
            return db == 'authentication'
        return None

class ForecastRouter:
    """
    A router to control all database operations on models in the forecasts app.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read forecast models go to forecast_db.
        """
        if model._meta.app_label == 'forecasts':
            return 'forecast_db'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write forecast models go to forecast_db.
        """
        if model._meta.app_label == 'forecasts':
            return 'forecast_db'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the forecasts app is involved.
        """
        if obj1._meta.app_label == 'forecasts' or obj2._meta.app_label == 'forecasts':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Ensure the forecasts app's models only appear in the forecast_db.
        """
        if app_label == 'forecasts':
            return db == 'forecast_db'
        return None

class AuthRouter:
    def allow_migrate(self, db, app_label, **hints):
        # Only allow 'auth' and 'account' migrations in 'auth_db'
        if app_label in ['auth', 'account']:
            return db == 'auth_db'
        return None
