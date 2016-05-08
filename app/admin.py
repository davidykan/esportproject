from django.contrib import admin

# Register your models here.
from .models import Entry, Game_table, Language_table, Favorites_table, Recent_table

class EntryAdmin(admin.ModelAdmin):
    list_display = ["source_id", "time", "viewers", "name_id", "name_display", "source", "title", "preview", "url", "status"]
    class Meta:
        model = Entry

admin.site.register(Entry, EntryAdmin)

class GameAdmin(admin.ModelAdmin):
    list_display = ["source_id_game", "game"]
    class Meta:
        model = Game_table

admin.site.register(Game_table, GameAdmin)

class LanguageAdmin(admin.ModelAdmin):
    list_display = ["source_id_language", "language"]
    class Meta:
        model = Language_table

admin.site.register(Language_table, LanguageAdmin)

class FavoritesAdmin(admin.ModelAdmin):
    list_display = ["source_id_user", "user"]
    class Meta:
        model = Language_table

admin.site.register(Favorites_table, FavoritesAdmin)

class RecentAdmin(admin.ModelAdmin):
    list_display = ["source_id_user", "user"]
    class Meta:
        model = Recent_table

admin.site.register(Recent_table, RecentAdmin)
