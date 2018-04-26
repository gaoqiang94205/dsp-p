import six

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            # print("构造{name}对象".format(name=name))
            return type.__new__(cls, name, bases, attrs)
        else:
            # print("构造{name}对象".format(name=name))
            # 找出类中定义的具有提示意义的Field类型类属性，放到__mappings__中，
            # 因为仅具有提示用户写代码的意义，所以可以从类属性中移除
            # 移除的目的是避免冲突：实例属性会覆盖同名的类属性
            mappings = {}
            fields = {}
            pk = None
            for k, v in attrs.items():
                if isinstance(v, Field):
                    if not v.name:
                        v.name = k
                    if v.pk:
                        if pk:
                            raise MultiplePrimaryKey("Found multiple primary key.")
                        pk = k
                    mappings[k] = v.name
                    fields[k] = v
            if not fields:
                raise NoField("no filed defined")
            for k in mappings.keys():
                attrs.pop(k)
            if not pk:
                pk = min(fields.items(), key=lambda i: i[1].creation_order)[0]
            attrs['__mappings__'] = mappings  # __mappings__只可能在Model的子类里
            attrs['__fields__'] = fields
            attrs['__table__'] = attrs.get('__table__') or inflection.tableize(name)
            attrs['__pk__'] = pk

            return type.__new__(cls, name, bases, attrs)
@six.add_metaclass(ModelMetaclass)
class Model(dict):
    __kv_store__ = PluginStore()

    def __init__(self, **kwargs):
        super(Model, self).__init__(**kwargs)
        for k, f in self.__fields__.items():
            self[k] = f.check_type(f.init(kwargs.get(k)))

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(
                r"'{name}' object has no attribute {key}".format(name=self.__class__.__name__, key=key))

    def __setattr__(self, key, value):
        self[key] = value

    def __repr__(self):
        return "<{name} '{pk}'>".format(name=self.__class__.__name__, pk=self.pk)

    def to_dict(self):
        ret = {}
        for k, v in dict(self).items():
            if k in self.__mappings__:
                ret[self.__mappings__[k]] = v
        return ret

    def to_view_dict(self):
        raise NotImplementedError()

    def marshall(self):
        return cPickle.dumps(self.to_dict())

    @classmethod
    def unmarshall(cls, serialized):
        d = cPickle.loads(str(serialized))
        data = {}
        for k, v in cls.__mappings__.items():
            data[k] = d[v]
        return cls(**data)

    @property
    def pk(self):
        return self[self.__pk__]

    @classmethod
    def _gen_key(cls, pk):
        return 'Models/{name}/{pk}'.format(name=cls.__name__, pk=pk)

    def save(self, prevExist=True):
        for k, f in self.__fields__.items():
            f.check_type(self[k])
        self.__kv_store__.set(self._gen_key(self.pk), self.marshall(), prevExist=prevExist)
        return self

    def delete(self):
        try:
            return self.unmarshall(self.__kv_store__.delete(self._gen_key(self.pk)))
        except KeyNotExist:
            raise PkNotExist("primary key %s not exist" % self.pk)

    @classmethod
    def query_raw(cls, pk_prefix=''):
        return cls.__kv_store__.getp(cls._gen_key(pk_prefix))

    @classmethod
    def query(cls, pk_prefix=''):
        return [cls.unmarshall(s) for s in cls.query_raw(pk_prefix).values()]

    @classmethod
    def get_raw(cls, pk):
        return cls.__kv_store__.get(cls._gen_key(pk))

    @classmethod
    def get(cls, pk, default=None):
        raw = cls.get_raw(pk)
        if raw is None:
            return default
        return cls.unmarshall(raw)

    @classmethod
    def exist(cls, pk, default=None):
        return cls.__kv_store__.exist(cls._gen_key(pk))
