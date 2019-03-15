
class ModelMixin:
    def to_dict(self,*exclude):
        '''将model转化成一个属性字典，
        ，exclude需要排除的字段名'''

        attr_dict = {}
        for field in self._meta.fields:
            field_name = field.attname
            if field_name not in exclude:
                attr_dict[field_name] = getattr(self,field_name)
        return attr_dict

