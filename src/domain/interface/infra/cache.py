from abc import ABC, abstractmethod
from typing import Any, List, Optional


class ICacheAsyncClient(ABC):
    """Interface para cliente de cache."""

    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """
        Recupera um valor do cache pela chave.
        
        Args:
            key: A chave para recuperar o valor
            
        Returns:
            O valor armazenado ou None se não existir
        """
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Armazena um valor no cache.
        
        Args:
            key: A chave para armazenar o valor
            value: O valor a ser armazenado
            ttl: Tempo de vida em segundos (opcional)
            
        Returns:
            True se armazenado com sucesso, False caso contrário
        """
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        """
        Remove um valor do cache.
        
        Args:
            key: A chave a ser removida
            
        Returns:
            True se removido com sucesso, False caso contrário
        """
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        Verifica se uma chave existe no cache.
        
        Args:
            key: A chave a verificar
            
        Returns:
            True se existe, False caso contrário
        """
        pass

    @abstractmethod
    async def clear(self) -> bool:
        """
        Limpa todo o cache.
        
        Returns:
            True se limpo com sucesso, False caso contrário
        """
        pass

    @abstractmethod
    async def mget(self, keys: List[str]) -> dict:
        """
        Recupera múltiplos valores do cache.
        
        Args:
            keys: Lista de chaves a recuperar
            
        Returns:
            Dicionário com as chaves e seus valores
        """
        pass

    @abstractmethod
    async def mset(self, data: dict, ttl: Optional[int] = None) -> bool:
        """
        Armazena múltiplos valores no cache.
        
        Args:
            data: Dicionário com chaves e valores
            ttl: Tempo de vida em segundos (opcional)
            
        Returns:
            True se armazenado com sucesso, False caso contrário
        """
        pass
    
    @abstractmethod
    async def append_to_list(self, key: str, value: dict, ttl: Optional[int] = None) -> int:
        """
        Armazena múltiplos valores no cache.
        
        Args:
            data: Dicionário com chaves e valores
            ttl: Tempo de vida em segundos (opcional)
            
        Returns:
            True se armazenado com sucesso, False caso contrário
        """
        pass

    @abstractmethod
    async def retrieve_and_delete(self, key: str) -> List[dict]:
        """
        Retorna o valor no cache e deleta.
        
        Args:
            key: Chave            
            
        Returns:
            List of dict se armazenado com sucesso, False caso contrário
        """
        pass




