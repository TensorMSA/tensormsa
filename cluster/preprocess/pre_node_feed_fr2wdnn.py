from cluster.preprocess.pre_node_feed import PreNodeFeed
import tensorflow as tf


class PreNodeFeedFr2Wdnn(PreNodeFeed):
    """

    """
    def run(self, conf_data):
        """
        override init class
        """
        super(PreNodeFeedFr2Wdnn, self).run(conf_data)
        self._init_node_parm(conf_data['node_id'])

    def _convert_data_format(self, obj, index):
        pass

    def create_feature_columns(self, dataconf = None):
        # Sparse base columns.
            # cate < class 'list'>: ['workclass', 'occupation', 'relationship', 'native_country', 'marital_status', 'sex',
            #                   'education', 'race']

       # cinti < class 'list'>: ['hours_per_week', 'age', 'capital_loss', 'capital_gain', 'education_num']

        gender = tf.contrib.layers.sparse_column_with_keys(
            column_name="sex", keys=["female", "male"])
        race = tf.contrib.layers.sparse_column_with_keys(
            column_name="race", keys=[
                "Amer-Indian-Eskimo",
                "Asian-Pac-Islander",
                "Black",
                "Other",
                "White"
            ])

        education = tf.contrib.layers.sparse_column_with_hash_bucket(
            "education", hash_bucket_size=1000)
        marital_status = tf.contrib.layers.sparse_column_with_hash_bucket(
            "marital_status", hash_bucket_size=100)
        relationship = tf.contrib.layers.sparse_column_with_hash_bucket(
            "relationship", hash_bucket_size=100)
        workclass = tf.contrib.layers.sparse_column_with_hash_bucket(
            "workclass", hash_bucket_size=100)
        occupation = tf.contrib.layers.sparse_column_with_hash_bucket(
            "occupation", hash_bucket_size=1000)
        native_country = tf.contrib.layers.sparse_column_with_hash_bucket(
            "native_country", hash_bucket_size=1000)

        # Continuous base columns.
        age = tf.contrib.layers.real_valued_column("age", dtype=tf.int64)
        education_num = tf.contrib.layers.real_valued_column("education_num", dtype=tf.int64)
        capital_gain = tf.contrib.layers.real_valued_column("capital_gain", dtype=tf.int64)
        capital_loss = tf.contrib.layers.real_valued_column("capital_loss", dtype=tf.int64)
        hours_per_week = tf.contrib.layers.real_valued_column("hours_per_week", dtype=tf.int64)

        label = tf.contrib.layers.real_valued_column("label", dtype=tf.int64)

        return set([
            workclass,
            education,
            marital_status,
            occupation,
            relationship,
            race,
            gender,
            native_country,
            age,
            education_num,
            capital_gain,
            capital_loss,
            hours_per_week,
            label,
        ])

    def input_fn(self, mode, data_file, batch_size, dataconf = None):
        try:
            input_features = self.create_feature_columns()
            features = tf.contrib.layers.create_feature_spec_for_parsing(input_features)

            feature_map = tf.contrib.learn.io.read_batch_record_features(
                file_pattern=[data_file],
                #file_pattern=data_file,
                batch_size=batch_size,
                features=features,
                name="read_batch_features_{}".format(mode))
            # sess = tf.InteractiveSession()
            # print(feature_map["age"].eval())
            # sess.close()
            #  with tf.Session() as sess:
            #    print(sess.run(feature_map["age"]))
            #     print(feature_map["age"].eval())

            # a = feature_map
            # sess = tf.Session()
            # sess.run(a)
            #x = tf.Print(feature_map['age'], [feature_map['age']])
            #print(x)

            target = feature_map.pop("label")

            #num_epoch =
            print(str(batch_size))
        except Exception as e:
            raise e

        return feature_map, target

        def input_fn2(self, mode, data_file, df, nnid, dataconf):
            """Wide & Deep Network input tensor maker
                V1.0    16.11.04    Initial
                    :param df : dataframe from hbase
                    :param df, nnid
                    :return: tensor sparse, constraint """
            try:
                self.df_validation(df, dataconf)

                # remove NaN elements
                df = df.dropna(how='any', axis=0)
                # df_test = df_test.dropna(how='any', axis=0)

                ##Make List for Continuous, Categorical Columns
                CONTINUOUS_COLUMNS = []
                CATEGORICAL_COLUMNS = []
                ##Get datadesc Continuous and Categorical infomation from Postgres nninfo
                # json_string = self.get_json_by_nnid(nnid) # DATACONF
                # json_object = json_string

                j_feature = dataconf['cell_feature']
                for cn, c_value in j_feature.items():
                    if c_value["column_type"] == "CATEGORICAL":
                        CATEGORICAL_COLUMNS.append(cn)
                    elif c_value["column_type"] == "CONTINUOUS":
                        CONTINUOUS_COLUMNS.append(cn)
                    elif c_value["column_type"] == "CATEGORICAL_KEY":
                        CATEGORICAL_COLUMNS.append(cn)

                        # {"data_conf": {"label": {"income_bracket": "LABEL"}, "cross_cell": {"col1": ["occupation", "education"], "col2": ["native_country", "occupation"]}, "cell_feature": {"age": {"column_type": "CONTINUOUS"}, "race": {"column_type": "CATEGORICAL"}, "gender": {"keys": ["female", "male"], "column_type": "CATEGORICAL_KEY"}, "education": {"column_type": "CATEGORICAL"}, "workclass": {"column_type": "CATEGORICAL"}, "occupation": {"column_type": "CATEGORICAL"}, "capital_gain": {"column_type": "CONTINUOUS"}, "capital_loss": {"column_type": "CONTINUOUS"}, "relationship": {"column_type": "CATEGORICAL"}, "education_num": {"column_type": "CONTINUOUS"}, "hours_per_week": {"column_type": "CONTINUOUS"}, "marital_status": {"column_type": "CATEGORICAL"}, "native_country": {"column_type": "CATEGORICAL"}}, "Transformations": {"col1": {"boundaries": [18, 25, 30, 35, 40, 45, 50, 55, 60, 65], "column_name": "age"}}}}
                # Check Continuous Column is exsist?
                if len(CONTINUOUS_COLUMNS) > 0:
                    # print(CONTINUOUS_COLUMNS)

                    continuous_cols = {k: tf.constant(df[k].values) for k in CONTINUOUS_COLUMNS}
                # Check Categorical Column is exsist?
                if len(CATEGORICAL_COLUMNS) > 0:

                    for k in CATEGORICAL_COLUMNS:
                        df[k] = df[k].astype('str')

                    categorical_cols = {k: tf.SparseTensor(
                        indices=[[i, 0] for i in range(df[k].size)],
                        values=df[k].values,
                        dense_shape=[df[k].size, 1])
                                        for k in CATEGORICAL_COLUMNS}

                # Merges the two dictionaries into one.
                feature_cols = {}
                if (len(CONTINUOUS_COLUMNS) > 0):
                    feature_cols.update(continuous_cols)
                if len(CATEGORICAL_COLUMNS) > 0:
                    feature_cols.update(categorical_cols)


                # dataconf
                LABEL_COLUMN = 'label'
                df[LABEL_COLUMN] = (df['income_bracket'].apply(lambda x: '>50K' in x)).astype(int)




                label = tf.constant(df["label"].values)

                return feature_cols, label
            except Exception as e:
                print("Error Message : {0}".format(e))
                raise Exception(e)
