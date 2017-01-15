from common.data.data_master import DataMaster

class DataS3Manager(DataMaster) :

    def get_schema_list(self):
        return None

    def post_schema_list(self, name):
        return None

    def update_schema_list(self, x_name, u_name):
        return None

    def delete_schema_list(self, name):
        return None

    def get_table_list(self, schema_name):
        return None

    def post_table_list(self, schema_name, table_name):
        return None

    def update_table_list(self, schema_name, x_name, u_name):
        return None

    def delete_table_list(self, schema_name, table_name):
        return None

    def get_contents(self):
        return None

    def post_contents(self, schema_name, table_name, context):
        return None

    def update_contents(self, schema_name, table_name, context):
        return None

    def delete_contents(self, schema_name, table_name):
        return None


