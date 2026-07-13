from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, CartItem, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'stock', 'online_exclusive')
    list_display_links = ('image_preview', 'name')
    list_filter = ('category', 'online_exclusive')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 20
    fieldsets = (
        ('Product Info', {
            'fields': ('name', 'slug', 'category', 'description', 'price', 'stock', 'online_exclusive'),
        }),
        ('Product Photo', {
            'description': 'Upload or replace the product image here. Choose a new file to update the photo.',
            'fields': ('image',),
        }),
    )

    @admin.display(description='Photo')
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:4px;" />',
                obj.image.url,
            )
        return '—'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'owner')
    list_filter = ('user',)
    search_fields = ('product__name', 'user__username')
    readonly_fields = ('user', 'session_key', 'product', 'quantity')
    fields = ('product', 'quantity', 'user', 'session_key')

    @admin.display(description='Owner')
    def owner(self, obj):
        if obj.user:
            return obj.user.username
        return 'Guest cart'

    def has_add_permission(self, request):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'total_amount', 'created_at', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('created_at',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'price', 'quantity')
    readonly_fields = ('order', 'product', 'price', 'quantity')
    search_fields = ('product__name', 'order__id')
