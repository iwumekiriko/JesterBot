import asyncio
import aiohttp
from typing import Optional, Dict, Any, Union

from src.logger import get_logger

from src.settings import API_PATH, DEVELOPMENT
from src.utils._exceptions import (
    CustomException,
    NotEnoughMoneyException,
    NoActiveBoosterException,
    BoosterAlreadyActiveException,
    AlreadyOwnsRoleException,
    NotEnoughItemsException,
    LootboxRoleAlreadyExistsException,
    LootboxRoleDoesNotExistException,
    ShopRoleAlreadyExistsException,
    ShopRoleDoesNotExistException,
    ShopKeyAlreadyExistsException,
    ShopKeyDoesNotExistException,
    AllShopTriesAreUsedException,
    LastTryDidntEndException,
    QuestTemplateAlreadyExistsException,
    QuestTemplateDoesNotExistException,
    NoAvailableGifs,
    APIException
)


logger = get_logger()


api_exceptions: Dict[str, type[APIException]] = {
    "00000": APIException,
    "00317": NotEnoughMoneyException,
    "00059": BoosterAlreadyActiveException,
    "00058": NoActiveBoosterException,
    "01403": AlreadyOwnsRoleException,
    "00242": NotEnoughItemsException,
    "00767": LootboxRoleAlreadyExistsException,
    "00769": LootboxRoleDoesNotExistException,
    "00589": ShopRoleAlreadyExistsException,
    "00590": ShopRoleDoesNotExistException,
    "00377": ShopKeyAlreadyExistsException,
    "00378": ShopKeyDoesNotExistException,
    "09921": AllShopTriesAreUsedException,
    "09922": LastTryDidntEndException,
    "01717": QuestTemplateAlreadyExistsException,
    "01718": QuestTemplateDoesNotExistException,
    "00622": NoAvailableGifs
}


class APIClient:
    """
    API client for convenient interaction with an API.

    This class provides methods to perform HTTP requests (GET, POST, PUT, DELETE)
    to interact with the API. The base URL for the API is configured in `src/settings.API_PATH`.

    Examples:
        >>> async with APIClient() as client:
            response = await client.get/post/put/delete("endpoint")
    """
    _instance = None
    _lock = asyncio.Lock()

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_APIClient__initialized') or not self.__initialized:
            self.__base_url = API_PATH
            self.__headers = {
                "Content-Type": "application/json"
            }
            self.__session = None
            self.__initialized = True

    async def ensure_session(self):
        async with self._lock:
            if self.__session is None or self.__session.closed:
                self.__session = aiohttp.ClientSession()

    async def __aenter__(self):
        await self.ensure_session()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    async def close(self):
        if self.__session and not self.__session.closed:
            await self.__session.close()
            self.__session = None

    async def resolve_request(
        self,
        endpoint: str,
        method: str = 'GET',
        query_params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute HTTP request to API endpoint.

        Args:
            endpoint (str): API endpoint path
            method (str): HTTP method (GET/POST/PUT/DELETE)
            query_params (Optional[Dict[str, Any]]): Query parameters
            body (Optional[Dict[str, Any]]): Request body

        Returns:
            Dict[str, Any]: JSON response from server

        Examples:
            >>> await make_request("users", "POST", body={"name": "John"})
            {"id": 1, "name": "John"}
        """
        await self.ensure_session()

        url = f"{self.__base_url}/{endpoint}"
        ssl = not DEVELOPMENT

        try:
            async with self.__session.request( # type: ignore
                method,
                url,
                params=query_params,
                json=body,
                headers=self.__headers,
                ssl=ssl
            ) as response:
                logger.info("Received a response from API [CODE: %s] | %s |: %s",
                             response.status, endpoint, await response.text() or "null")

                if response.status == 400:
                    error_data = await response.json()
                    code = error_data.get("code", "00000")
                    raise api_exceptions[code](**error_data)

                if response.status == 204:
                    return None

                if response.status != 200:
                    raise CustomException(
                        f"{endpoint} is not responding. Status code: **{response.status}**.")

                return await response.json()
        except aiohttp.ClientError as e:
            raise CustomException(f"Network error: {str(e)}")

    async def get(
        self,
        endpoint: str,
        query_params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute GET request.
        
        Args:
            endpoint (str): API endpoint path
            query_params (Optional[Dict[str, Any]]): Query parameters
            
        Returns:
            Dict[str, Any]: JSON response from server
                
        Examples:
            >>> await get("users", {"id": 1})
            {"id": 1, "name": "John"}
        """
        return await self.resolve_request(
            endpoint,
            method="GET",
            query_params=query_params
        )
    
    async def post(
        self,
        endpoint: str,
        body: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute POST request.
        
        Args:
            endpoint (str): API endpoint path
            body (Optional[Dict[str, Any]]): Request body
            query_params (Optional[Dict[str, Any]]): Query parameters
            
        Returns:
            Dict[str, Any]: JSON response from server
            
        Examples:
            >>> await post("users", body={"name": "Jane"})
            {"id": 2, "name": "Jane"}
        """
        return await self.resolve_request(
            endpoint,
            method="POST",
            body=body,
            query_params=query_params
        )
    
    async def put(
        self,
        endpoint: str,
        body: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute PUT request.

        Args:
            endpoint (str): API endpoint path.
            body (Optional[Dict[str, Any]]): Request body to send (for updating resources).
            query_params (Optional[Dict[str, Any]]): Query parameters to include in the request.

        Returns:
            Dict[str, Any]: JSON response from the server.

        Examples:
            >>> await put("users/1", body={"name": "John Doe"})
            {"id": 1, "name": "John Doe"}
        """
        return await self.resolve_request(
            endpoint,
            method="PUT",
            body=body,
            query_params=query_params
        )
    
    async def delete(
        self,
        endpoint: str,
        body: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Execute DELETE request.

        Args:
            endpoint (str): API endpoint path.
            body (Optional[Dict[str, Any]]): Request body to send (for updating resources).
            query_params (Optional[Dict[str, Any]]): Query parameters to include in the request.

        Returns:
            Dict[str, Any]: JSON response from the server.

        Examples:
            >>> await delete("users/1")
            {"status": "success", "message": "User deleted"}
        """
        return await self.resolve_request(
            endpoint,
            method="DELETE",
            body=body,
            query_params=query_params
        )