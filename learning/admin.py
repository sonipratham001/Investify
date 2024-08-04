from django.contrib import admin
from .models import Video, Course, Quiz, Webinar, LearningPath, Stock, Portfolio, Trade
from .models import Question, Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [OptionInline]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Video)
admin.site.register(Course)
admin.site.register(Quiz)
admin.site.register(Webinar)
admin.site.register(LearningPath)
admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Trade)
