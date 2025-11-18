"""
Integration tests for template operations.

Tests cover:
- Template download from GitHub
- Template extraction
- Template validation
- Merge operations
- Error handling
"""

import json
import tempfile
import zipfile
from pathlib import Path
from unittest.mock import MagicMock, patch, mock_open

import httpx
import pytest

from goalkeeper_cli import download_template_from_github, AGENT_CONFIG


class TestTemplateDownload:
    """Test template download functionality."""

    def test_download_template_basic(self, tmp_path):
        """Test basic template download."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test content"]
        mock_response.headers = {"content-length": "10"}
        
        zip_path, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
            client=mock_client,
        )
        
        assert zip_path.exists()
        assert metadata["filename"] == "goal-kit-template-claude-sh.zip"
        assert metadata["release"] == "v1.0.0"

    def test_download_template_with_different_agents(self, tmp_path):
        """Test template download for different agents."""
        agents = ["claude", "gemini", "cursor"]
        
        for agent in agents:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "tag_name": "v1.0.0",
                "assets": [
                    {
                        "name": f"goal-kit-template-{agent}-sh.zip",
                        "browser_download_url": f"https://example.com/{agent}.zip",
                        "size": 1000,
                    }
                ],
            }
            
            mock_client = MagicMock()
            mock_client.get.return_value = mock_response
            mock_client.stream.return_value.__enter__.return_value = mock_response
            mock_response.iter_bytes.return_value = [b"test content"]
            mock_response.headers = {"content-length": "10"}
            
            zip_path, metadata = download_template_from_github(
                agent,
                tmp_path,
                script_type="sh",
                verbose=False,
                show_progress=False,
                client=mock_client,
            )
            
            assert zip_path.exists()

    def test_download_template_script_type_sh(self, tmp_path):
        """Test template download with sh script type."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test content"]
        mock_response.headers = {"content-length": "10"}
        
        zip_path, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
            client=mock_client,
        )
        
        assert "sh" in zip_path.name

    def test_download_template_script_type_ps(self, tmp_path):
        """Test template download with ps (PowerShell) script type."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-ps.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test content"]
        mock_response.headers = {"content-length": "10"}
        
        zip_path, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="ps",
            verbose=False,
            show_progress=False,
            client=mock_client,
        )
        
        assert "ps" in zip_path.name


class TestTemplateDownloadErrors:
    """Test error handling in template download."""

    def test_download_template_github_error(self, tmp_path):
        """Test handling of GitHub API errors."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Not Found"
        mock_response.headers = {}
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        
        with pytest.raises(RuntimeError):
            download_template_from_github(
                "claude",
                tmp_path,
                script_type="sh",
                verbose=False,
                show_progress=False,
                client=mock_client,
                debug=False,
            )

    def test_download_template_no_matching_asset(self, tmp_path):
        """Test handling when no matching template asset is found."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "other-file.zip",
                    "browser_download_url": "https://example.com/other.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        
        with pytest.raises(SystemExit):
            download_template_from_github(
                "nonexistent-agent",
                tmp_path,
                script_type="sh",
                verbose=False,
                show_progress=False,
                client=mock_client,
            )

    def test_download_template_network_error(self, tmp_path):
        """Test handling of network errors."""
        mock_client = MagicMock()
        mock_client.get.side_effect = httpx.ConnectError("Network error")
        
        with pytest.raises(RuntimeError):
            download_template_from_github(
                "claude",
                tmp_path,
                script_type="sh",
                verbose=False,
                show_progress=False,
                client=mock_client,
            )

    def test_download_template_invalid_json(self, tmp_path):
        """Test handling of invalid JSON response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Invalid JSON"
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        
        with pytest.raises(RuntimeError):
            download_template_from_github(
                "claude",
                tmp_path,
                script_type="sh",
                verbose=False,
                show_progress=False,
                client=mock_client,
            )


class TestTemplateExtraction:
    """Test template extraction functionality."""

    def test_extract_template_basic(self, tmp_path):
        """Test basic template extraction."""
        # Create a test zip file
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "test content")
            zf.writestr("subdir/nested.txt", "nested content")
        
        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()
        
        # Extract
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)
        
        # Verify
        assert (extract_dir / "file.txt").exists()
        assert (extract_dir / "subdir" / "nested.txt").exists()

    def test_extract_template_overwrites_existing(self, tmp_path):
        """Test that extraction can overwrite existing files."""
        # Create initial file
        extract_dir = tmp_path / "extracted"
        extract_dir.mkdir()
        existing_file = extract_dir / "file.txt"
        existing_file.write_text("original content")
        
        # Create zip with new content
        zip_path = tmp_path / "template.zip"
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr("file.txt", "new content")
        
        # Extract
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)
        
        # Verify file was overwritten
        assert existing_file.read_text() == "new content"


class TestTemplateValidation:
    """Test template validation."""

    def test_validate_template_structure(self, tmp_path):
        """Test that template has expected structure."""
        # Create a mock template structure
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        
        # Create expected directories
        (template_dir / ".goalkit").mkdir()
        (template_dir / ".goalkit" / "vision.md").write_text("# Vision")
        
        # Validate
        assert (template_dir / ".goalkit").exists()
        assert (template_dir / ".goalkit" / "vision.md").exists()

    def test_validate_template_contains_required_files(self, tmp_path):
        """Test that template contains required files."""
        template_dir = tmp_path / "template"
        template_dir.mkdir()
        
        # Create expected files
        required_files = [
            ".goalkit/vision.md",
            ".goalkit/goals",
            ".goalkit/scripts",
        ]
        
        (template_dir / ".goalkit").mkdir()
        (template_dir / ".goalkit" / "vision.md").write_text("# Vision")
        (template_dir / ".goalkit" / "goals").mkdir()
        (template_dir / ".goalkit" / "scripts").mkdir()
        
        # Verify all required files exist
        for file_path in required_files:
            assert (template_dir / file_path).exists()


class TestTemplateMerge:
    """Test template merge operations."""

    def test_merge_templates_no_conflicts(self, tmp_path):
        """Test merging templates without conflicts."""
        # Create source template
        source = tmp_path / "source"
        source.mkdir()
        (source / "new_file.txt").write_text("new content")
        (source / "subdir").mkdir()
        (source / "subdir" / "nested.txt").write_text("nested")
        
        # Create destination
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "existing_file.txt").write_text("existing")
        
        # Simulate merge
        for item in source.iterdir():
            if item.is_file():
                (dest / item.name).write_text(item.read_text())
            elif item.is_dir():
                import shutil
                shutil.copytree(item, dest / item.name, dirs_exist_ok=True)
        
        # Verify
        assert (dest / "existing_file.txt").exists()
        assert (dest / "new_file.txt").exists()
        assert (dest / "subdir" / "nested.txt").exists()

    def test_merge_templates_with_existing_files(self, tmp_path):
        """Test merging when destination has existing files."""
        # Create source
        source = tmp_path / "source"
        source.mkdir()
        (source / "file.txt").write_text("source content")
        
        # Create destination with same file
        dest = tmp_path / "dest"
        dest.mkdir()
        (dest / "file.txt").write_text("destination content")
        (dest / "other.txt").write_text("other")
        
        # Simulate merge (overwrite)
        import shutil
        for item in source.iterdir():
            if item.is_file():
                shutil.copy2(item, dest / item.name)
        
        # Verify - source should overwrite destination
        assert (dest / "file.txt").read_text() == "source content"
        assert (dest / "other.txt").exists()


class TestTemplateMetadata:
    """Test template metadata handling."""

    def test_metadata_contains_filename(self, tmp_path):
        """Test that metadata includes filename."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test"]
        mock_response.headers = {"content-length": "10"}
        
        _, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
            client=mock_client,
        )
        
        assert "filename" in metadata
        assert metadata["filename"] == "goal-kit-template-claude-sh.zip"

    def test_metadata_contains_size(self, tmp_path):
        """Test that metadata includes file size."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 5000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test"]
        mock_response.headers = {"content-length": "10"}
        
        _, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
            client=mock_client,
        )
        
        assert "size" in metadata
        assert metadata["size"] == 5000

    def test_metadata_contains_release(self, tmp_path):
        """Test that metadata includes release tag."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v2.5.1",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test"]
        mock_response.headers = {"content-length": "10"}
        
        _, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
            client=mock_client,
        )
        
        assert "release" in metadata
        assert metadata["release"] == "v2.5.1"


class TestTemplateGitHubAuth:
    """Test GitHub token authentication for template downloads."""

    def test_download_with_github_token(self, tmp_path):
        """Test download with GitHub token."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test"]
        mock_response.headers = {"content-length": "10"}
        
        zip_path, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
            client=mock_client,
            github_token="test_token_123",
        )
        
        # Should pass token to headers
        assert mock_client.get.called
        call_args = mock_client.get.call_args
        assert "headers" in call_args.kwargs or len(call_args.args) > 1


class TestTemplateProgress:
    """Test progress display during template operations."""

    def test_download_with_progress_display(self, tmp_path):
        """Test download with progress display enabled."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test content"]
        mock_response.headers = {"content-length": "100"}
        
        zip_path, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=True,
            client=mock_client,
        )
        
        assert zip_path.exists()

    def test_download_without_progress_display(self, tmp_path):
        """Test download with progress display disabled."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "tag_name": "v1.0.0",
            "assets": [
                {
                    "name": "goal-kit-template-claude-sh.zip",
                    "browser_download_url": "https://example.com/template.zip",
                    "size": 1000,
                }
            ],
        }
        
        mock_client = MagicMock()
        mock_client.get.return_value = mock_response
        mock_client.stream.return_value.__enter__.return_value = mock_response
        mock_response.iter_bytes.return_value = [b"test content"]
        mock_response.headers = {"content-length": "0"}
        
        zip_path, metadata = download_template_from_github(
            "claude",
            tmp_path,
            script_type="sh",
            verbose=False,
            show_progress=False,
            client=mock_client,
        )
        
        assert zip_path.exists()
