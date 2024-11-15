class AuthenticationRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.model_name == 'session':
            return 'authentication'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'auth' or model._meta.model_name == 'session':
            return 'authentication'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if (
            obj1._meta.app_label == 'auth' or obj2._meta.app_label == 'auth' or
            obj1._meta.model_name == 'session' or obj2._meta.model_name == 'session'
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'auth' or model_name == 'session':
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
