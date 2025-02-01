import pytest

from unittest.mock import patch
from app.src.api.services.collections_service import CollectionsService

@pytest.mark.asyncio
async def test_list_collections():
    # Arrange
    mock_response = {
        'CollectionIds': [],
        'NextToken': 'token123'
    }
    
    with patch('boto3.client') as mock_boto:
        mock_boto.return_value.list_collections.return_value = mock_response
        service = CollectionsService()
        
        # Act
        result = await service.list_collections()
        
        # Assert
        assert result == mock_response
        mock_boto.return_value.list_collections.assert_called_once()

@pytest.mark.asyncio
async def test_list_collections_error():
    with patch('boto3.client') as mock_boto:
        mock_boto.return_value.list_collections.side_effect = Exception('AWS Error')
        service = CollectionsService()
        
        with pytest.raises(Exception):
            await service.list_collections()
