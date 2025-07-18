from api.calls.schemas import HelloResponse


class HelloService:
    """
    Service class for handling hello world logic
    """

    @staticmethod
    def get_hello_message(name: str = None) -> HelloResponse:
        """
        Generate a hello world message
        
        Args:
            name: Optional name to include in greeting
            
        Returns:
            dict: Contains the hello message and metadata
        """
        if name:
            message = f"Hello {name}! Welcome to CityGlow Calls API"
        else:
            message = "Hello World! Welcome to CityGlow Calls API"

        return HelloResponse(
            message=message,
            service="calls",
            version="1.0.0",
            status="active"
        )
