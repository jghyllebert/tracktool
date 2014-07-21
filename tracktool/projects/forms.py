from django import forms

from .models import Project


class UpdateStateForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('current_state',)


class UpdateFlowForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ('contract', 'product', 'notes', 'flow', 'current_state', 'is_ended', 'end_date')

    def __init__(self, *args, **kwargs):
        super(UpdateFlowForm, self).__init__(*args, **kwargs)
        self.project_instance = None
        if self.instance:
            self.project_instance = self.instance
        extra = self.project_instance.flow.splitlines()
        for i, todo in enumerate(extra):
            if todo.find('#') == -1:
                self.fields['todo_%i' % i] = forms.BooleanField(
                    required=False,
                    label="%s" % todo)
            else:
                self.fields['todo_%i' % i] = forms.BooleanField(
                    required=False,
                    label="%s" % todo[1:],
                    initial=True
                )

    def save(self, commit=True):
        project = super(UpdateFlowForm, self).save(commit=False,)
        flow = project.flow.splitlines()

        check = []
        option = []
        for i, todo in enumerate(flow):
            check.append(i)
            option.append(todo)
            if self.cleaned_data['todo_%i' % i]:
                # Add identifier field is active, remove old one
                # only change when state changed
                if todo.find('#') == -1:
                    flow.insert(i + 1, "#%s" % todo)
                    flow.pop(i)
            else:
                if todo.find('#') >= 0:
                    flow.insert(i + 1, "%s" % todo[1:])
                    flow.pop(i)

        # save flow, meanwhile check state of every checkpoint
        workflow = ""
        count_finished = 0
        for todo in flow:
            workflow += todo + "\n"
            if todo.find('#') >= 0:
                count_finished += 1
        project.flow = workflow

        #i from enumerate should equal in count to be ended
        if count_finished == i + 1:
            project.is_ended = True

        if commit:
            project.save()

        return project