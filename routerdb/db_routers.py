class AuthRouter:

    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels = ['auth','admin','sessions','contenttypes']

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to netgsm.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to netgsm.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or

            obj2._meta.app_label in self.route_app_labels

        ):

           return True

        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'netgsm' database.
        """
        if app_label in self.route_app_labels:

            return db == 'default'

        return None

class SportsIntRouter:
    """
    A router to control all database operations on models in the
    sportsint applications.
    """
    route_app_labels = ['sportsint']
    def db_for_read(self, model, **hints):
        """
        Attempts  go to sportsint.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'sportsint'

        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write  models go to sportsint.
        """
        if model._meta.app_label in self.route_app_labels:
            return 'sportsint'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the sportsint apps is
        involved.
        """
        if (
            obj1._meta.app_label in self.route_app_labels or

            obj2._meta.app_label in self.route_app_labels
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):

        """
        Make sure the sportsint apps only appear in the
        'sportsint' database.
        """
        if app_label in self.route_app_labels:
            return db == 'sportsint'
        return None
