# web_app/forms.py
from django import forms
from .models import BioDecagonMono, BioDecagonCombo, \
    Handelsnamen_drugs


# This function retrieves a list of medication choices from the Handelsnamen_drugs model, formats it for Django's
# ChoiceField with an initial empty option
def get_medication_choices():
    choices = Handelsnamen_drugs.objects.values_list('STITCH', 'Name')
    medication_choices = [('', 'Select Medication')] + [(stitch, name.strip()) for stitch, name in choices]

    # Debugging-Ausgabe
    print(f"Medication Choices: {medication_choices}")

    return medication_choices


# This class, DynamicChoiceField, is designed to dynamically update its choices based on the number of medications
# selected
class DynamicChoiceField(forms.ModelMultipleChoiceField):
    def _init_(self, *args, **kwargs):
        # Initialize the DynamicChoiceField, calling the base class constructor
        super().__init__(*args, **kwargs)

    def update_choices(self, num_medications):
        # Update choices based on the number of medications selected
        if num_medications == 1:
            queryset = BioDecagonMono.objects.all()
        elif num_medications == 2:
            queryset = BioDecagonCombo.objects.all()
        else:
            queryset = BioDecagonMono.objects.none()

        self.queryset = queryset
        self.choices = self.queryset.values_list('Side_Effect_Name', 'Side_Effect_Name').distinct()


# The form provides a structured way to capture user input related to medication selection and side effect information.
class MedicationSelectionForm(forms.Form):
    num_medications = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

    medication_1_name = forms.ChoiceField(
        choices=[('', 'Select Medication')] + get_medication_choices(),
        label='Medication 1 Name',
    )

    medication_2_name = forms.ChoiceField(
        choices=[('', 'Select Medication')] + get_medication_choices(),
        label='Medication 2 Name',
        required=False,
    )

    # Neue Felder für Benutzereingaben zu Nebenwirkungen
    individual_side_effect = forms.CharField(label='Individual Side Effect', required=False)
    polypharmacy_side_effects = forms.CharField(label='Polypharmacy Side Effects', required=False)
    side_effect_name = forms.CharField(label='Side Effect Name', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Setze das leere Element für die Auswahl von Medikament 2
        self.fields['medication_2_name'].choices = [('', 'Select Medication')] + self.fields[
                                                                                     'medication_2_name'].choices[1:]

        # Debugging-Ausgabe
        print(self.fields['medication_1_name'].choices)
        print(self.fields['medication_2_name'].choices)


# This form class is designed for reporting user-specific side effects and includes hidden fields for medication
# names along with validation for user inputs. The clean method performs additional validation checks for required
# fields.
class ReportOwnSideEffectsForm(forms.Form):
    # Hidden input fields to store medication names
    medication_name_1 = forms.CharField(widget=forms.HiddenInput(), required=True)
    medication_name_2 = forms.CharField(widget=forms.HiddenInput(), required=False)
    # Fields for user input on side effects
    individual_side_effect = forms.CharField(label='Individual Side Effect', required=True)
    polypharmacy_side_effects = forms.CharField(label='Polypharmacy Side Effects', required=True)
    side_effect_name = forms.CharField(label='Side Effect Name', required=True)

    def __init__(self, *args, **kwargs):
        # Pop medication names from kwargs to set initial values
        medication_name_1 = kwargs.pop('medication_name_1', None)
        medication_name_2 = kwargs.pop('medication_name_2', None)

        # Call the base class constructor
        super(ReportOwnSideEffectsForm, self).__init__(*args, **kwargs)

        # Set initial values for hidden fields
        self.fields['medication_name_1'].initial = medication_name_1
        self.fields['medication_name_2'].initial = medication_name_2

        # Set values for hidden fields in widget attributes to ensure rendering
        self.fields['medication_name_1'].widget.attrs['value'] = medication_name_1
        self.fields['medication_name_2'].widget.attrs['value'] = medication_name_2

    def clean(self):
        # Call the clean method of the base class to perform standard cleaning
        cleaned_data = super().clean()

        # Validation for individual_side_effect
        individual_side_effect = cleaned_data.get('individual_side_effect')
        if not individual_side_effect:
            self.add_error('individual_side_effect', 'This field is required.')

        # Validdation for polypharmacy_side_effects
        polypharmacy_side_effects = cleaned_data.get('polypharmacy_side_effects')

        # Validation for side_effect_name
        side_effect_name = cleaned_data.get('side_effect_name')
        if not side_effect_name:
            self.add_error('side_effect_name', 'This field is required.')

        return cleaned_data


# This form class is designed for selecting multiple side effects and includes a hidden field for storing the number
# of medications. The get_side_effect_choices method retrieves and combines unique side effects from two models,
# and the clean_side_effect_names method ensures that the selected side effects are returned as cleaned data.
class SideEffectSelectionForm(forms.Form):
    # Hidden input field to store the number of medications
    num_medications = forms.IntegerField(widget=forms.HiddenInput(), initial=1)

    # Multiple choice field for selecting side effects
    side_effect_names = forms.MultipleChoiceField(choices=[], label='Side Effect Names', widget=forms.SelectMultiple())

    def __init__(self, *args, **kwargs):
        # Call the base class constructor
        super().__init__(*args, **kwargs)

        # Set num_medications to 2 if not provided in initial data
        num_medications = self.initial.get('num_medications', 2)

        # Set choices for side_effect_names based on the number of medications
        self.fields['side_effect_names'].choices = self.get_side_effect_choices(num_medications)

    def get_side_effect_choices(self, num_medications):
        # Extract all unique side effects from BioDecagonMono and BioDecagonCombo
        side_effects_mono = BioDecagonMono.objects.values_list('Side_Effect_Name', flat=True).distinct()
        side_effects_combo = BioDecagonCombo.objects.values_list('Side_Effect_Name', flat=True).distinct()

        # Combine side effects from both tables
        all_side_effects = set(side_effects_mono) | set(side_effects_combo)

        # Sort side effects alphabetically, considering None values
        all_side_effects = sorted(all_side_effects, key=lambda x: (x is None, x))

        return [(effect, effect) for effect in all_side_effects]

    def clean_side_effect_names(self):
        # Retrieve the selected side effects from cleaned data
        selected_side_effects = self.cleaned_data['side_effect_names']
        return selected_side_effects
