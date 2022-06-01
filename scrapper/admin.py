from django.contrib import admin

from scrapper.models.api_key import ApiKey
from scrapper.models.collected_data import CollectedData
from scrapper.models.folder import Folder
from scrapper.models.selector_type import SelectorType
from scrapper.models.selectors import Selector
from scrapper.models.timezone import Timezone
from scrapper.models.user import User
from scrapper.models.website import Website


@admin.register(Timezone)
class TimezoneAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(ApiKey)
class ApiKeyAdmin(admin.ModelAdmin):
    pass


@admin.register(CollectedData)
class CollectedDataAdmin(admin.ModelAdmin):
    pass


@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    pass


@admin.register(SelectorType)
class SelectorTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Selector)
class SelectorAdmin(admin.ModelAdmin):
    pass
