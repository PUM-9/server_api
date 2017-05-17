from django import forms


class MeshJobForm(forms.Form):
    name = forms.CharField(max_length=200, label="Name")
    log_level = forms.ChoiceField(choices=(("0", "Trace"),
                                           ("1", "Debug"),
                                           ("2", "Info"),
                                           ("3", "Warning"),
                                           ("4", "Error")), initial='2', label="Log level")
    file = forms.FileField(label='Point Cloud')


class RegistrationJobForm(forms.Form):
    name = forms.CharField(max_length=200, label="Name")
    log_level = forms.ChoiceField(choices=(("0", "Trace"),
                                           ("1", "Debug"),
                                           ("2", "Info"),
                                           ("3", "Warning"),
                                           ("4", "Error")), initial='2', label="Log level")
    max_correspondence = forms.DecimalField(min_value=0, initial=10, label="Max Correspondence")
    max_iterations = forms.IntegerField(min_value=1, max_value=200, initial=100, label="Max iterations")
    transformation_epsilon = forms.DecimalField(min_value=0, max_value=10, initial=0.00000001,
                                                label="Transformation Epsilon")
    leaf_size = forms.DecimalField(min_value=0, max_value=100, initial=0.43, label="Leaf Size")
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label="Point Clouds")
