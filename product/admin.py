from django.contrib import admin
from .models import Product, Review, Category
from django.utils import timezone
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from product.resources import ReviewResource





class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1
    classes = ('collapse',)
    # min_num = 3
    # max_num = 20


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "create_date", "is_in_stock", "update_date", "added_days_ago", "how_many_reviews", "bring_img_to_list")    
    list_editable = ( 'name', "is_in_stock")
    list_display_links = ("create_date", )
    list_filter = ("is_in_stock", "create_date")
    ordering = ("name",) 
    search_fields = ("name",) 
    prepopulated_fields = {'slug' : ('name',)}
    list_per_page = 25
    date_hierarchy = "update_date"
    inlines = (ReviewInline,)
    readonly_fields = ("bring_image",)
    # fields = (('name', 'slug'), 'description', "is_in_stock") 
    fieldsets = (
        (None, {
            "fields": (
                ('name', 'slug'), "is_in_stock" # to display multiple fields on the same line, wrap those fields in their own tuple
            ),
            # 'classes': ('wide', 'extrapretty'), wide or collapse
        }),
        ('Optionals Settings', {
            "classes" : ("collapse", ),
            "fields" : ("description", "categories", "product_img", "bring_image"),
            'description' : "You can use this section for optionals settings"
        })
    )
    actions = ("is_in_stock", )

    def is_in_stock(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f"{count} products added to stock.")
    
    is_in_stock.short_description = 'add to stock'

    def added_days_ago(self, product):
        fark = timezone.now() - product.create_date
        return fark.days

    def bring_img_to_list(self, obj):
        if obj.product_img:
            return mark_safe(f"<img src={obj.product_img.url} width=50 height=50></img>")
        return mark_safe("******")
    bring_img_to_list.short_description = "product_image"

admin.site.register(Product, ProductAdmin)


class ReviewAdmin(ImportExportModelAdmin):
    autocomplete_fields = ("product",)
    list_display = ('__str__', 'created_date', 'is_released')
    list_per_page = 50
    resource_class = ReviewResource
    # raw_id_fields = ('product',) 

admin.site.register(Review, ReviewAdmin)
admin.site.register(Category)


admin.site.site_title = "Clarusway Title"
admin.site.site_header = "Clarusway Admin Portal"  
admin.site.index_title = "Welcome to Clarusway Admin Portal"
