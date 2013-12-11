from django import forms

class UserInterval(forms.Form):
    initialValue = "Month"
    intervals = [
                ("Min","Min"),
                ("Hour","Hour"),
                ("Day","Day"),
                ("Week","Week"),
                ("Month","Month"),
                ("Year","Year")
                ]
    choiceLabel = "Please Select Interval and Click Submit"

    interval = forms.ChoiceField(choices = intervals, label = choiceLabel, initial = initialValue)
