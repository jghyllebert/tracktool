from django import forms
from django.forms.models import inlineformset_factory

from .models import Contract, Payment
from projects.models import Project


class ContractForm(forms.ModelForm):
    shoot_location_is_same_as_billing_address = forms.BooleanField(required=False)

    class Meta:
        model = Contract
        fields = ('client', 'shoot_location_is_same_as_billing_address', 'shoot_address',
                  'shoot_city', 'shoot_zip_code', 'contract_number', 'contract_date', 'total_cost', 'payment_options')

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['client'].required = False

    def clean_contract_number(self):
        contract_number = self.cleaned_data.get('contract_number')
        client = self.cleaned_data.get('client')

        if client:
            # check if contract number already exists in country
            contract_number_exists = Contract.objects.filter(
                contract_number=contract_number,
                client__country=client.country
            ).exists()

            if contract_number_exists:
                raise forms.ValidationError(u"Contract number already exists in country %(country_name)s" %
                                            {'country_name': client.country.name}
                )

        return contract_number


ContractProjectsFormSet = inlineformset_factory(Contract, Project, fields=('product', 'notes'), extra=2,
                                                can_delete=False)


class UpdatePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'reference', 'contract', 'inputter')
        widgets = {
            'inputter': forms.HiddenInput(),
            'contract': forms.HiddenInput()
        }


class UpdateContractForm(forms.ModelForm):

    class Meta:
        model = Contract
        fields = ('client', 'shoot_address',
                  'shoot_city', 'shoot_zip_code', 'contract_number', 'contract_date', 'total_cost', 'payment_options')

    def clean_contract_number(self):
        contract_number = self.cleaned_data.get('contract_number')
        client = self.cleaned_data.get("client")
        if contract_number != self.instance.contract_number:
            # check if contract number already exists in country
            contract_number_exists = Contract.objects.filter(
                contract_number=contract_number,
                client__country=client.country
            ).exists()

            if contract_number_exists:
                raise forms.ValidationError(
                    u"Contract number already exists in country %(country_name)s" %
                    {'country_name': client.country.name}
                )

        return contract_number

    def __init__(self, *args, **kwargs):
        super(UpdateContractForm, self).__init__(*args, **kwargs)
        self.fields['contract_date'].widget.attrs['class'] = 'form-control'