from rest_framework.schemas import SchemaGenerator

class CustomSchemaGenerator(SchemaGenerator):
    title = 'REST API Index'

    def get_link(self, path, method, view):
        try :
            link = super(CustomSchemaGenerator, self).get_link(path, method, view)
            link._fields += self.get_core_fields(view)
            return link
        except Exception as e :
            return None

    def get_core_fields(self, view):
        if(len(getattr(view, 'coreapi_fields', ())) > 0 ) :
            return getattr(view, 'coreapi_fields', ())
        else :
            return getattr(view, '', ())