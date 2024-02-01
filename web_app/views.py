# web_app/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import MedicationSelectionForm, ReportOwnSideEffectsForm, SideEffectSelectionForm
from .models import BioDecagonMono, BioDecagonCombo, Handelsnamen_drugs, UserAccessHistory


# the home function is defined as a view for the home page
def home(request):
    if request.method == 'POST':
        form = MedicationSelectionForm(request.POST)
        if form.is_valid():
            num_medications = form.cleaned_data['num_medications']

            # Fügt Eintrag in die UserAccessHistory Tabelle hinzu
            UserAccessHistory.objects.create(
                user=request.user,
                action=f"{num_medications} Medikament(e) ausgewählt"
            )

            if num_medications == 1:
                return redirect('select_medications', num_medications=num_medications)
            elif num_medications == 2:
                return redirect('select_medications', num_medications=num_medications)
    else:
        form = MedicationSelectionForm()

    return render(request, 'base.html', {'form': form})


# In the select_medications view, if the POST request is valid,
# it updates the form with selected medication names, logs the user's action, and redirects to 'report_side_effects'
def select_medications(request):
    if request.method == 'POST':
        form = MedicationSelectionForm(request.POST)
        if form.is_valid():
            num_medications = form.cleaned_data['num_medications']
            medication_name_1 = form.cleaned_data['medication_1_name']

            # ausgewählte Medikamentennamen als Hidden Field zum Formular hinzugeefügt
            form.fields['medication_name_1'].initial = medication_name_1

            medication_name_2 = form.cleaned_data.get('medication_2_name')

            # Fügt Eintrag in die UserAccessHistory Tabelle hinzu
            UserAccessHistory.objects.create(
                user=request.user,
                action=f"{num_medications} Medikament(e) ausgewählt: {medication_name_1}, {medication_name_2}"
            )
            if num_medications == 2 and medication_name_2:
                # Den zweiten ausgewählten Medikamentennamen ebenfalls als Hidden Field zum Formular hinzugefügt
                form.fields['medication_name_2'].initial = medication_name_2

            return redirect('report_side_effects')

    else:
        form = MedicationSelectionForm()

    return render(request, 'select_medications.html', {'form': form})


# if the HTTP request method is POST, it retrieves selected medication names, determines the number of medications,
# and fetches corresponding data from the database. It logs the user's action in the UserAccessHistory table and
# renders the 'show_side_effects.html' template with information about the medications and their associated side
# effects.
def show_side_effects(request):
    if request.method == 'POST':
        medication_name_1 = request.POST.get('medication_1_name')
        medication_name_2 = request.POST.get('medication_2_name')

        num_medications = 1 if medication_name_2 is None else 2

        try:
            medication_1 = Handelsnamen_drugs.objects.get(STITCH=medication_name_1)
        except Handelsnamen_drugs.DoesNotExist:
            print(f"Medication 1 with STITCH={medication_name_1} does not exist.")
            medication_1 = None

        try:
            medication_2 = Handelsnamen_drugs.objects.get(STITCH=medication_name_2)
        except Handelsnamen_drugs.DoesNotExist:
            print(f"Medication 2 with STITCH={medication_name_2} does not exist.")
            medication_2 = None

        # Fügt Eintrag in die UserAccessHistory Tabelle hinzu
        UserAccessHistory.objects.create(
            user=request.user,
            action=f"Nebenwirkungen für {num_medications} Medikament(e) angesehen: {medication_name_1}, {medication_name_2}"
        )

        if num_medications == 1 and medication_1:
            side_effects = BioDecagonMono.objects.filter(STITCH=medication_1.STITCH).values(
                'Individual_Side_Effect', 'Side_Effect_Name')

            # Debugging Ausgabe
            print(f'STITCH: {medication_1.STITCH}')
            print(f'Side Effects: {side_effects}')

        elif num_medications == 2 and medication_1 and medication_2:
            side_effects = BioDecagonCombo.objects.filter(STITCH1=medication_1.STITCH,
                                                          STITCH2=medication_2.STITCH).values(
                'Polypharmacy_Side_Effects', 'Side_Effect_Name')
        else:
            side_effects = []

        return render(request, 'show_side_effects.html', {'num_medications': num_medications,
                                                          'medication_name_1': medication_name_1,
                                                          'medication_name_2': medication_name_2,
                                                          'side_effects': side_effects})

    return render(request, 'select_medications.html')


# The form ReportOwnSideEffectsForm is initialized, and if the HTTP request method is POST, it processes the form
# data. It retrieves medication names, logs the user's action in the UserAccessHistory table, and creates a new entry
# in the database for reported side effects. Depending on the number of medications selected, it either creates a
# record in the BioDecagonMono or BioDecagonCombo model.
def report_side_effects(request):
    form = ReportOwnSideEffectsForm()

    if request.method == 'POST':
        medication_name_1 = request.POST.get('medication_name_1')
        medication_name_2 = request.POST.get('medication_name_2')

        # Check if medication_name_2 is not None before using it in the condition
        num_medications = 1 if medication_name_2 is None or medication_name_2 == 'None' else 2

        UserAccessHistory.objects.create(
            user=request.user,
            action=f"Nebenwirkungen für {num_medications} Medikament(e) gemeldet: {medication_name_1}, {medication_name_2}"
        )

        print(f"medication_name_1: {medication_name_1}")
        print(f"medication_name_2: {medication_name_2}")
        print(f"num: {num_medications}")

        try:
            medication_1 = Handelsnamen_drugs.objects.get(STITCH=medication_name_1)
        except Handelsnamen_drugs.DoesNotExist:
            print(f"Medication 1 with STITCH={medication_name_1} does not exist.")
            medication_1 = None

        try:
            medication_2 = Handelsnamen_drugs.objects.get(STITCH=medication_name_2)
        except Handelsnamen_drugs.DoesNotExist:
            print(f"Medication 2 with STITCH={medication_name_2} does not exist.")
            medication_2 = None

        if num_medications == 1 and medication_1:
            print(f'STITCH: {medication_1.STITCH}')
            BioDecagonMono.objects.create(
                STITCH=medication_1.STITCH if medication_1 else None,
                Individual_Side_Effect=request.POST.get('individual_side_effect'),
                Side_Effect_Name=request.POST.get('side_effect_name')
            )
            return render(request, 'report_side_effects.html',
                          {'form': form, 'num_medications': num_medications,
                           'medication_name_1': medication_name_1, 'medication_name_2': medication_name_2})

        elif num_medications == 2 and medication_1 and medication_2:
            print(f'STITCH1: {medication_1.STITCH}, STITCH2: {medication_2.STITCH}')
            BioDecagonCombo.objects.create(
                STITCH1=medication_1.STITCH if medication_1 else None,
                STITCH2=medication_2.STITCH if medication_2 else None,
                Polypharmacy_Side_Effects=request.POST.get('polypharmacy_side_effects'),
                Side_Effect_Name=request.POST.get('side_effect_name')
            )
            return render(request, 'report_side_effects.html',
                          {'form': form, 'num_medications': num_medications,
                           'medication_name_1': medication_name_1, 'medication_name_2': medication_name_2})
    else:
        form = ReportOwnSideEffectsForm()

    return render(request, 'report_side_effects.html', {'form': form})


# #######################################################################################################################################
# #######################################################################################################################################


# if the HTTP request method is POST, it validates the form data and processes the selected side effects. It logs the
# user's action in the UserAccessHistory table, stores the number of medications and selected side effects in the
# session, and queries the database for relevant side effect information based on the selected medications.
# Additionally, it calls the perform_medication_analysis function to analyze the best matching medications and
# renders the 'analysis_results.html' template with the results.
def analysis_report_symptoms(request):
    if request.method == 'POST':
        form = SideEffectSelectionForm(request.POST)
        if form.is_valid():
            num_medications = form.cleaned_data['num_medications']
            selected_side_effects = form.cleaned_data['side_effect_names']

            # Fügt Eintrag in die UserAccessHistory Tabelle hinzu
            UserAccessHistory.objects.create(
                user=request.user,
                action=f"Symptomanalyse für {num_medications} Medikament(e) durchgeführt: {', '.join(selected_side_effects)}"
            )

            # Speichere die Anzahl der Medikamente in der Sitzung
            request.session['num_medications'] = num_medications
            print("num medications:", num_medications)

            # Speichern Sie die ausgewählten Nebenwirkungen in der Sitzung
            request.session['selected_side_effects'] = list(selected_side_effects)
            # Debugging-Ausgabe, um die ausgewählten Nebenwirkungen anzuzeigen
            print("Selected Side Effects:", selected_side_effects)

            side_effects = []  # Initialisiere side_effects

            if num_medications == 2:
                print("num medications: 2")
                print("Selected Side Effects:", selected_side_effects)
                side_effects = BioDecagonCombo.objects.filter(Side_Effect_Name__in=selected_side_effects)
                side_effect_names = side_effects.values_list('Side_Effect_Name', flat=True)
                print("Side Effects from BioDecagonCombo:", side_effect_names)
                print("Number of side effects:", side_effects.count())

            elif num_medications == 1:
                side_effects = BioDecagonMono.objects.filter(Side_Effect_Name__in=selected_side_effects)
                print("num medications: 1")
                print("Selected Side Effects:", selected_side_effects)
                print("Side Effects from BioDecagonMono:", side_effects)

            # Debugging-Ausgabe
            print("Final side_effects:", side_effects)

            # Rufe die Funktion auf, um die besten übereinstimmenden Medikamente zu analysieren
            matching_medications = perform_medication_analysis(request)

            return render(request, 'analysis_results.html',
                          {'selected_side_effects': selected_side_effects, 'side_effects': side_effects,
                           'matching_medications': matching_medications})

    else:
        form = SideEffectSelectionForm()
        return HttpResponse()  # Hier wird eine leere HttpResponse-Instanz zurückgegeben

    return render(request, 'analysis_report_system.html', {'form': form})


########################################################################################################################
########################################################################################################################
# Functions for the analysis model

# takes selected side effects, a medication model, and the number of medications as parameters. It queries the
# database to obtain medications with the selected side effects, calculates a matching score based on common side
# effects, and returns a sorted list of matching medications.
def find_best_matching_medications(selected_side_effects, medication_model, num_medications):
    matching_medications = {}

    # Retrieve medications from the specified medication_model that have at least one of the selected side effects.
    medications = medication_model.objects.filter(Side_Effect_Name__in=selected_side_effects)

    for medication in medications:
        # Convert the list of side effects associated with the current medication to a set for efficient intersection
        # calculations.
        medication_side_effects = set(medication.side_effects_list())

        # Determine the key for identifying the medication and model based on the number of medications selected.
        if num_medications == 1:
            # Stitch column from BioDecagonMono
            key = (medication.STITCH,)

        elif num_medications == 2:
            # Stitch column from BioDecagonCombo
            key = (medication.STITCH1, medication.STITCH2)

        # The score is calculated based on the number of matching side effects between the selected side effects and
        # the side effects associated with a specific medication.
        matching_side_effects = set(selected_side_effects) & medication_side_effects
        score = len(matching_side_effects)
        print("mm_side-effects:", matching_side_effects)
        print(score)

        # Scores are aggregated for medications with the same key, updating the total score if the key already exists.
        if key not in matching_medications:
            matching_medications[key] = (score,)
        else:
            matching_medications[key] = (matching_medications[key][0] + score,)

    # Sort the medications based on their aggregated scores in descending order, with medications having higher
    # scores appearing first in the sorted list.
    sorted_matching_medications = sorted(matching_medications.items(), key=lambda x: x[1][0], reverse=True)
    print("sorted mm:", sorted_matching_medications)

    return sorted_matching_medications


# This function performs medication analysis based on the number of medications selected, using the
# find_best_matching_medications function.
def perform_medication_analysis(request):
    # Retrieve selected side effects and the number of medications from the session
    selected_side_effects = request.session.get('selected_side_effects', [])
    num_medications = request.session.get('num_medications', 0)

    # Check if essential data is missing
    if not selected_side_effects or not num_medications:
        print("Error: Selected side effects or num_medications is missing.")
        return None

    try:
        # Perform medication analysis based on the number of medications selected
        if num_medications == 1:
            matching_medications = find_best_matching_medications(selected_side_effects, BioDecagonMono, 1)
        elif num_medications == 2:
            matching_medications = find_best_matching_medications(selected_side_effects, BioDecagonCombo, 2)
        else:
            print("Error: Invalid value for num_medications.")
            return None
        # Vor dem Rendern der HTML-Seite
        print("Matching Medications:", matching_medications)

        return matching_medications
    except Exception as e:
        # Handle any exceptions that may occur during the analysis
        print(f"Error: {e}")
        return None
