"""Tests for templates module.

Tests template downloading, extraction, and merging functionality.
"""

import json
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

import pytest
from goalkeeper_cli.templates import TemplateMetadata, TemplateManager


class TestTemplateMetadata:
    """Test TemplateMetadata class."""
    
    def test_metadata_creation(self):
        """Test creating TemplateMetadata instance."""
        meta = TemplateMetadata(
            filename="goal-kit-template-claude-sh.zip",
            size=15234,
            release="v1.2.0",
            asset_url="https://github.com/..."
        )
        
        assert meta.filename == "goal-kit-template-claude-sh.zip"
        assert meta.size == 15234
        assert meta.release == "v1.2.0"
        assert meta.asset_url == "https://github.com/..."
    
    def test_metadata_to_dict(self):
        """Test converting metadata to dictionary."""
        meta = TemplateMetadata(
            filename="test.zip",
            size=1000,
            release="v1.0",
            asset_url="http://example.com"
        )
        
        data = meta.to_dict()
        assert data["filename"] == "test.zip"
        assert data["size"] == 1000
        assert data["release"] == "v1.0"
        assert data["asset_url"] == "http://example.com"


class TestTemplateManager:
    """Test TemplateManager class."""
    
    def test_manager_creation(self):
        """Test creating TemplateManager instance."""
        manager = TemplateManager()
        
        assert manager.repo_owner == "Nom-nom-hub"
        assert manager.repo_name == "goal-kit"
        assert manager.client is not None
        assert manager.console is not None
    
    def test_manager_with_custom_client(self):
        """Test creating manager with custom client."""
        custom_client = Mock()
        manager = TemplateManager(client=custom_client)
        
        assert manager.client is custom_client
    
    def test_find_matching_asset_exact_match(self):
        """Test finding matching asset with exact match."""
        release_data = {
            "assets": [
                {"name": "goal-kit-template-claude-sh.zip", "browser_download_url": "http://example.com/1"},
                {"name": "goal-kit-template-copilot-ps.zip", "browser_download_url": "http://example.com/2"},
            ]
        }
        
        manager = TemplateManager()
        asset = manager._find_matching_asset(release_data, "claude", "sh", verbose=False)
        
        assert asset is not None
        assert asset["name"] == "goal-kit-template-claude-sh.zip"
    
    def test_find_matching_asset_no_match(self):
        """Test finding asset when no match exists."""
        release_data = {
            "assets": [
                {"name": "goal-kit-template-claude-sh.zip"},
            ]
        }
        
        manager = TemplateManager()
        asset = manager._find_matching_asset(release_data, "invalid", "sh", verbose=False)
        
        assert asset is None
    
    def test_find_matching_asset_fallback(self):
        """Test finding asset with fallback to any template."""
        # When no exact match, fallback to first available template (verbose=True to trigger return)
        release_data = {
            "assets": [
                {"name": "some-other-file.zip"},
                {"name": "goal-kit-template-generic-sh.zip", "browser_download_url": "http://example.com/default"},
            ]
        }
        
        manager = TemplateManager()
        asset = manager._find_matching_asset(release_data, "unknown", "ps", verbose=True)
        
        # Should find the fallback template (any goal-kit-template-*.zip)
        assert asset is not None
        assert "goal-kit-template-" in asset["name"]
    
    def test_auth_headers_with_token(self):
        """Test generating auth headers with token."""
        headers = TemplateManager._get_auth_headers("test_token_123")
        
        assert "Authorization" in headers
        assert headers["Authorization"] == "Bearer test_token_123"
    
    def test_auth_headers_without_token(self):
        """Test generating auth headers without token."""
        headers = TemplateManager._get_auth_headers(None)
        
        assert headers == {}
    
    def test_deep_merge_simple(self):
        """Test merging simple dictionaries."""
        base = {"a": 1, "b": 2}
        update = {"c": 3}
        
        result = TemplateManager._deep_merge(base, update)
        
        assert result == {"a": 1, "b": 2, "c": 3}
    
    def test_deep_merge_overwrite(self):
        """Test that new values overwrite existing ones."""
        base = {"a": 1, "b": 2}
        update = {"b": 20}
        
        result = TemplateManager._deep_merge(base, update)
        
        assert result == {"a": 1, "b": 20}
    
    def test_deep_merge_nested(self):
        """Test merging nested dictionaries."""
        base = {"config": {"key1": "value1", "key2": "value2"}}
        update = {"config": {"key2": "new_value2", "key3": "value3"}}
        
        result = TemplateManager._deep_merge(base, update)
        
        assert result == {
            "config": {
                "key1": "value1",
                "key2": "new_value2",
                "key3": "value3"
            }
        }
    
    def test_deep_merge_list_replacement(self):
        """Test that lists are replaced, not merged."""
        base = {"items": [1, 2, 3]}
        update = {"items": [4, 5]}
        
        result = TemplateManager._deep_merge(base, update)
        
        assert result == {"items": [4, 5]}
    
    def test_merge_settings_new_file(self):
        """Test merging settings for new file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = Path(temp_dir) / "nonexistent.json"
            new_content = {"key": "value"}
            
            result = TemplateManager.merge_settings(settings_path, new_content)
            
            assert result == {"key": "value"}
    
    def test_merge_settings_existing_file(self):
        """Test merging settings for existing file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = Path(temp_dir) / "settings.json"
            
            # Create existing file
            existing = {"a": 1, "b": 2}
            with open(settings_path, "w") as f:
                json.dump(existing, f)
            
            new_content = {"b": 20, "c": 3}
            result = TemplateManager.merge_settings(settings_path, new_content)
            
            assert result == {"a": 1, "b": 20, "c": 3}
    
    def test_merge_settings_invalid_json(self):
        """Test merging settings with invalid existing JSON."""
        with tempfile.TemporaryDirectory() as temp_dir:
            settings_path = Path(temp_dir) / "settings.json"
            
            # Create invalid JSON file
            with open(settings_path, "w") as f:
                f.write("not valid json{")
            
            new_content = {"key": "value"}
            result = TemplateManager.merge_settings(settings_path, new_content)
            
            # Should return new content when existing is invalid
            assert result == {"key": "value"}
    
    def test_extract_zip(self):
        """Test extracting zip file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create a simple zip file
            zip_path = temp_path / "test.zip"
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.writestr("file1.txt", "content1")
                zf.writestr("subdir/file2.txt", "content2")
            
            # Extract to destination
            dest_path = temp_path / "extracted"
            TemplateManager.extract(zip_path, dest_path)
            
            # Verify extraction
            assert (dest_path / "file1.txt").exists()
            assert (dest_path / "subdir" / "file2.txt").exists()
            
            with open(dest_path / "file1.txt") as f:
                assert f.read() == "content1"
    
    def test_extract_nonexistent_zip(self):
        """Test extracting non-existent zip file raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / "nonexistent.zip"
            dest_path = Path(temp_dir) / "dest"
            
            with pytest.raises(RuntimeError):
                TemplateManager.extract(zip_path, dest_path)


class TestTemplateDownload:
    """Test template download functionality."""
    
    @patch("goalkeeper_cli.templates.httpx.Client")
    def test_download_success(self, mock_client_class):
        """Test successful template download."""
        # Mock the client
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        # Mock GitHub API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.2.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "size": 15234,
                    "browser_download_url": "http://example.com/template.zip"
                }
            ]
        }
        mock_response.iter_bytes.return_value = [b"fake_zip_content"]
        
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        
        # Run download
        manager = TemplateManager()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path, metadata = manager.download(
                "claude",
                script_type="sh",
                verbose=False,
                show_progress=False
            )
            
            assert metadata.filename == "goal-kit-template-claude-sh.zip"
            assert metadata.size == 15234
            assert metadata.release == "v1.2.0"
    
    @patch("goalkeeper_cli.templates.httpx.Client")
    def test_download_github_api_error(self, mock_client_class):
        """Test handling GitHub API error."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_client.get.return_value = mock_response
        
        manager = TemplateManager()
        
        with pytest.raises(RuntimeError):
            manager.download("claude", verbose=False)
    
    @patch("goalkeeper_cli.templates.httpx.Client")
    def test_download_no_matching_asset(self, mock_client_class):
        """Test error when no matching asset found."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.2.0",
            "assets": []
        }
        mock_client.get.return_value = mock_response
        
        manager = TemplateManager()
        
        with pytest.raises(RuntimeError) as exc_info:
            manager.download("unknown_agent", verbose=False)
        
        assert "No matching release asset found" in str(exc_info.value)
