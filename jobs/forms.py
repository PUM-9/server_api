from django import forms


class RegistrationJobForm(forms.Form):
    name = forms.CharField(max_length=200)
    log_level = forms.ChoiceField(choices=(("0", "Trace"),
                                      ("1", "Debug"),
                                      ("2", "Info"),
                                      ("3", "Warning"),
                                      ("4", "Error")))
    max_correspondence = forms.DecimalField(min_value=0)
    max_iterations = forms.IntegerField(min_value=1, max_value=200)
    transformation_epsilon = forms.DecimalField(min_value=0, max_value=10)
    leaf_size = forms.DecimalField(min_value=0, max_value=100)
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
