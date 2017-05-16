from django import forms


class RegistrationJobForm(forms.Form):
    name = forms.CharField(max_length=200)
    log_level = forms.ChoiceField(choices=(("0", "Trace"),
                                           ("1", "Debug"),
                                           ("2", "Info"),
                                           ("3", "Warning"),
                                           ("4", "Error")), initial='2')
    max_correspondence = forms.DecimalField(min_value=0, initial=10)
    max_iterations = forms.IntegerField(min_value=1, max_value=200, initial=100)
    transformation_epsilon = forms.DecimalField(min_value=0, max_value=10, initial=0.00000001)
    leaf_size = forms.DecimalField(min_value=0, max_value=100, initial=0.43)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
