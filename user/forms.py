from django import forms


from user.models import  Profile
'''定义form表单，验证prfile传入参数的准确性'''
class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile #指定model参数所对应的model
        fields = [
        'dating_sex','location',
        'min_distance','max_distance',
        'min_dating_age','max_dating_age',
        'vibration','only_match','auto_play'
        ]

    def clean_max_distance(self):
        cleaned_data = super().clean()
        min_distance = cleaned_data['min_distance']
        max_distance = cleaned_data['max_distance']

        if min_distance > max_distance:
            raise  forms.ValidationError('min_distance 必须小于等于 max_distance')
        else:
            return max_distance

    def clean_max_dating_age(self):
        cleaned_data = super().clean()
        min_dating_age = cleaned_data['min_dating_age']
        max_dating_age = cleaned_data['max_dating_age']

        if min_dating_age > max_dating_age:
            raise  forms.ValidationError('min_dating_age 必须小于等于 max_dating_age')
        else:
            return max_dating_age