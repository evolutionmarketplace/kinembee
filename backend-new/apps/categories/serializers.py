"""
Serializers for categories.
"""
from rest_framework import serializers
from .models import Category, CategoryAttribute, CategoryTag


class CategoryAttributeSerializer(serializers.ModelSerializer):
    """
    Serializer for category attributes.
    """
    class Meta:
        model = CategoryAttribute
        fields = [
            'id', 'name', 'slug', 'attribute_type', 'is_required',
            'is_filterable', 'choices', 'min_value', 'max_value',
            'min_length', 'max_length'
        ]


class CategoryTagSerializer(serializers.ModelSerializer):
    """
    Serializer for category tags.
    """
    class Meta:
        model = CategoryTag
        fields = ['id', 'name', 'slug', 'color']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for categories.
    """
    children = serializers.SerializerMethodField()
    attributes = CategoryAttributeSerializer(many=True, read_only=True)
    tags = CategoryTagSerializer(many=True, read_only=True, source='tag_assignments.tag')
    full_path = serializers.ReadOnlyField()
    level = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 'image',
            'category_type', 'is_active', 'featured', 'product_count',
            'full_path', 'level', 'children', 'attributes', 'tags'
        ]

    def get_children(self, obj):
        if obj.get_children().exists():
            return CategorySerializer(obj.get_children(), many=True, context=self.context).data
        return []


class CategoryListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for category lists.
    """
    subcategory_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'icon', 'image', 'category_type',
            'product_count', 'subcategory_count', 'featured'
        ]

    def get_subcategory_count(self, obj):
        return obj.get_children().filter(is_active=True).count()


class CategoryTreeSerializer(serializers.ModelSerializer):
    """
    Serializer for category tree structure.
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'level', 'children']

    def get_children(self, obj):
        children = obj.get_children().filter(is_active=True)
        if children.exists():
            return CategoryTreeSerializer(children, many=True).data
        return []