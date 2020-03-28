from rest_framework.schemas import AutoSchema


class DefaultSchema(AutoSchema):
    def _allows_filters(self, path, method):
        """
        Override to remove filter field on all actions but list
        """
        if getattr(self.view, 'filter_backends', None) is None:
            return False

        if hasattr(self.view, 'action'):
            return self.view.action == 'list'

        return method.lower() == 'get'
