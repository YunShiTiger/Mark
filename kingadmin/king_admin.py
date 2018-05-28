from django import forms
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType

from assets import models

from kingadmin.admin_base import site, BaseKingAdmin

from django.shortcuts import render, HttpResponse



class AssetAdmin(BaseKingAdmin):
    list_display = (
        'id', 'asset_type', 'sn', 'name', 'manufactory',
        'management_ip', 'idc', 'business_unit', 'admin',
        'trade_date', 'status'
    )
    search_fields = ['sn', ]
    choice_fields = ('asset_type', 'status')
    fk_fields = ('manufactory', 'idc', 'business_unit', 'admin')
    list_per_page = 10
    list_filter = ('asset_type', 'status', 'manufactory', 'idc', 'business_unit', 'admin', 'trade_date')
    dynamic_fk = 'asset_type'
    dynamic_list_display = ('model', 'sub_asset_type', 'os_type', 'os_distribution')
    dynamic_choice_fields = ('sub_asset_type',)
    m2m_fields = ('tags',)

class IDCAdmin(BaseKingAdmin):
    list_display = ('id', 'name','log_details')
    list_per_page = 2
    # readonly_table = True
    actions = ["test", "delete_selected_objs"]

    def test(self, request, querysets):
        print("in test", )
        return HttpResponse('测试成功')

    test.short_description = "测试动作"

    def default_form_validation(self):
        print("-----customer validation ", self)
        print("----instance:", self.instance)

        consult_content = self.cleaned_data.get("name", '')
        if len(consult_content) < 4:
            return forms.ValidationError(
                ('Field %(field)s 不能少于4个字符'),
                code='invalid',
                params={'field': "name", },
            )

    def log_details(self):
        '''日志详情'''
        ele = '''<a href="/kingadmin/web/" >详情</a> '''
        return ele

    log_details.display_name = '日志详情'

class NicAdmin(BaseKingAdmin):
    list_display = ('name', 'macaddress', 'ipaddress', 'netmask', 'bonding')
    search_fields = ('macaddress', 'ipaddress')


class EventLogAdmin(BaseKingAdmin):
    list_display = ('name', 'colored_event_type', 'asset', 'component', 'detail', 'date', 'user')
    search_fields = ('asset',)
    list_filter = ('event_type', 'component', 'date', 'user')


class NewAssetApprovalZoneAdmin(BaseKingAdmin):
    list_display = ('sn', 'asset_type', 'manufactory', 'model', 'cpu_model', 'cpu_count', 'cpu_core_count', 'ram_size',
                    'os_distribution', 'os_release', 'date', 'approved', 'approved_by', 'approved_date')
    actions = ['approve_selected_objects']

    def approve_selected_objects(modeladmin, request, queryset):
        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
        ct = ContentType.objects.get_for_model(queryset.model)
        return HttpResponseRedirect("/asset/new_assets/approval/?ct=%s&ids=%s" % (ct.pk, ",".join(selected)))

    approve_selected_objects.short_description = "批准入库"


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        if len(password1) < 6:
            raise forms.ValidationError("Passwords takes at least 6 letters")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdmin(BaseKingAdmin):
    add_form = UserCreationForm

    list_display = ('id', 'name', 'email','token', 'department', 'tel','mobile','date_joined','valid_begin_time','valid_end_time')
    readonly_fields = ['password', 'name']

    search_fields = ['email', 'name']
    list_filter = ['name']
    change_page_onclick_fields = {
        'password': ['password', '重置密码']
    }


site.register(models.UserProfile, UserAdmin)
site.register(models.Asset, AssetAdmin)
site.register(models.NIC, NicAdmin)
site.register(models.IDC, IDCAdmin)
site.register(models.NewAssetApprovalZone, NewAssetApprovalZoneAdmin)
