from rest_framework import serializers


class HelloRequestSerializer(serializers.Serializer):
    """DRF serializer for documentation - mirrors HelloRequest Pydantic model"""
    name = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Name to personalize the greeting"
    )


class HelloResponseSerializer(serializers.Serializer):
    """DRF serializer for documentation - mirrors HelloResponse Pydantic model"""
    message = serializers.CharField(help_text="The greeting message")
    service = serializers.CharField(help_text="Service identifier")
    version = serializers.CharField(help_text="API version")
    status = serializers.CharField(help_text="Service status")
