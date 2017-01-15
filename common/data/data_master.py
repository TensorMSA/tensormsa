import importlib

class DataMaster :
    """

    """

    def load(self, class_name, module_name="common.data"):
        """
        return class with name 'targetting classes inherit DataMasterManager'
        -ex) DataMaster().load("DataS3Manager").get_schema_list()
        :param module_name:
        :param class_name:
        :return: Class
        """
        module = importlib.import_module(module_name)
        LoadClass = getattr(module, class_name)
        return LoadClass()

    def get_schema_list(self):
        pass

    def post_schema_list(self, name):
        pass

    def update_schema_list(self, x_name, u_name):
        pass

    def delete_schema_list(self, name):
        pass

    def get_table_list(self, schema_name):
        pass

    def post_table_list(self, schema_name, table_name):
        pass

    def update_table_list(self, schema_name, x_name, u_name):
        pass

    def delete_table_list(self, schema_name, table_name):
        pass

    def get_contents(self):
        pass

    def post_contents(self, schema_name, table_name, context):
        pass

    def update_contents(self, schema_name, table_name, context):
        pass

    def delete_contents(self, schema_name, table_name):
        pass

