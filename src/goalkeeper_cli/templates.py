"""Template management and downloading for Goalkeeper CLI.

Provides clean abstraction for template download, extraction, and merge operations.
Replaces monolithic template logic in __init__.py.
"""

import json
import zipfile
import tempfile
import shutil
import ssl
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

import httpx
import truststore
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


# SSL context setup
_ssl_context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)


class TemplateMetadata:
    """Metadata about a downloaded template.
    
    Attributes:
        filename: Name of the downloaded zip file
        size: File size in bytes
        release: Release tag/version
        asset_url: URL where template can be downloaded
    """
    
    def __init__(self, filename: str, size: int, release: str, asset_url: str):
        """Initialize template metadata."""
        self.filename = filename
        self.size = size
        self.release = release
        self.asset_url = asset_url
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "filename": self.filename,
            "size": self.size,
            "release": self.release,
            "asset_url": self.asset_url
        }


class TemplateManager:
    """Manage template downloads and extraction.
    
    Handles downloading templates from GitHub releases, extracting them,
    and merging configuration files.
    """
    
    def __init__(self, client: Optional[httpx.Client] = None, console: Optional[Console] = None):
        """Initialize template manager.
        
        Args:
            client: Optional httpx.Client instance (uses default if None)
            console: Optional Rich Console instance (uses default if None)
        """
        self.client = client or httpx.Client(verify=_ssl_context)
        self.console = console or Console()
        self.repo_owner = "Nom-nom-hub"
        self.repo_name = "goal-kit"
    
    def download(
        self,
        ai_assistant: str,
        script_type: str = "sh",
        verbose: bool = True,
        show_progress: bool = True,
        debug: bool = False,
        github_token: Optional[str] = None
    ) -> Tuple[Path, TemplateMetadata]:
        """Download template from GitHub releases.
        
        Args:
            ai_assistant: AI assistant name (e.g., 'claude', 'copilot')
            script_type: Script type ('sh' or 'ps')
            verbose: Whether to print status messages
            show_progress: Whether to show download progress
            debug: Whether to include debug details in errors
            github_token: Optional GitHub token for API requests
            
        Returns:
            Tuple of (zip_path, metadata)
            
        Raises:
            RuntimeError: If download fails
        """
        if verbose:
            self.console.print("[cyan]Fetching latest release information...[/cyan]")
        
        api_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/releases/latest"
        auth_headers = self._get_auth_headers(github_token)
        
        try:
            response = self.client.get(
                api_url,
                timeout=30,
                follow_redirects=True,
                headers=auth_headers,
            )
            
            if response.status_code != 200:
                msg = f"GitHub API returned {response.status_code} for {api_url}"
                if debug:
                    msg += f"\nResponse headers: {response.headers}\nBody (truncated 500): {response.text[:500]}"
                raise RuntimeError(msg)
            
            try:
                release_data = response.json()
            except ValueError as je:
                raise RuntimeError(
                    f"Failed to parse release JSON: {je}\nRaw (truncated 400): {response.text[:400]}"
                )
        
        except Exception as e:
            if isinstance(e, RuntimeError):
                raise
            raise RuntimeError(f"Failed to fetch GitHub releases: {str(e)}") from e
        
        # Find matching asset
        asset = self._find_matching_asset(release_data, ai_assistant, script_type, verbose)
        
        if asset is None:
            pattern = f"goal-kit-template-{ai_assistant}-{script_type}"
            asset_names = [a.get("name", "?") for a in release_data.get("assets", [])]
            msg = f"No matching release asset found for {ai_assistant} (expected pattern: {pattern})\nAvailable: {', '.join(asset_names)}"
            raise RuntimeError(msg)
        
        # Download the template
        download_url = asset["browser_download_url"]
        filename = asset["name"]
        file_size = asset["size"]
        
        if verbose:
            self.console.print(f"[cyan]Found template:[/cyan] {filename}")
            self.console.print(f"[cyan]Size:[/cyan] {file_size:,} bytes")
            self.console.print(f"[cyan]Release:[/cyan] {release_data['tag_name']}")
        
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = Path(temp_dir) / filename
            
            if verbose:
                self.console.print(f"[cyan]Downloading template...[/cyan]")
            
            self._download_file(
                download_url,
                zip_path,
                file_size,
                show_progress,
                debug,
                github_token,
                auth_headers
            )
            
            if verbose:
                self.console.print(f"Downloaded: {filename}")
            
            metadata = TemplateMetadata(
                filename=filename,
                size=file_size,
                release=release_data["tag_name"],
                asset_url=download_url
            )
            
            return zip_path, metadata
    
    def _find_matching_asset(self, release_data: dict, ai_assistant: str, script_type: str, verbose: bool) -> Optional[dict]:
        """Find matching template asset in release.
        
        Args:
            release_data: GitHub release data
            ai_assistant: AI assistant name
            script_type: Script type (sh or ps)
            verbose: Whether to print messages
            
        Returns:
            Asset dict if found, None otherwise
        """
        assets = release_data.get("assets", [])
        pattern = f"goal-kit-template-{ai_assistant}-{script_type}"
        
        # Try exact match first
        matching_assets = [
            asset for asset in assets
            if pattern in asset["name"] and asset["name"].endswith(".zip")
        ]
        
        if matching_assets:
            return matching_assets[0]
        
        # Try fallback to any template
        fallback_assets = [
            asset for asset in assets
            if asset["name"].startswith("goal-kit-template-") and asset["name"].endswith(".zip")
        ]
        
        if fallback_assets and verbose:
            self.console.print(
                f"[yellow]No specific template for {ai_assistant}, "
                f"using fallback template: {fallback_assets[0]['name']}[/yellow]"
            )
            return fallback_assets[0]
        
        return None
    
    def _download_file(
        self,
        url: str,
        dest_path: Path,
        total_size: int,
        show_progress: bool,
        debug: bool,
        github_token: Optional[str],
        auth_headers: dict
    ) -> None:
        """Download file with progress tracking.
        
        Args:
            url: URL to download
            dest_path: Destination file path
            total_size: Expected file size
            show_progress: Whether to show progress bar
            debug: Whether to include debug details
            github_token: GitHub token for auth
            auth_headers: Authorization headers
            
        Raises:
            RuntimeError: If download fails
        """
        try:
            with self.client.stream(
                "GET",
                url,
                timeout=60,
                follow_redirects=True,
                headers=auth_headers,
            ) as response:
                if response.status_code != 200:
                    body_sample = response.text[:400]
                    raise RuntimeError(
                        f"Download failed with {response.status_code}\n"
                        f"Headers: {response.headers}\nBody (truncated): {body_sample}"
                    )
                
                content_length = int(response.headers.get("content-length", 0))
                
                with open(dest_path, "wb") as f:
                    if content_length == 0:
                        # No size info, download without progress
                        for chunk in response.iter_bytes(chunk_size=8192):
                            f.write(chunk)
                    else:
                        # Show progress if requested
                        if show_progress:
                            with Progress(
                                SpinnerColumn(),
                                TextColumn("[progress.description]{task.description}"),
                                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                                console=self.console,
                            ) as progress:
                                task = progress.add_task("Downloading...", total=content_length)
                                downloaded = 0
                                for chunk in response.iter_bytes(chunk_size=8192):
                                    f.write(chunk)
                                    downloaded += len(chunk)
                                    progress.update(task, completed=downloaded)
                        else:
                            for chunk in response.iter_bytes(chunk_size=8192):
                                f.write(chunk)
        
        except Exception as e:
            if dest_path.exists():
                dest_path.unlink()
            if isinstance(e, RuntimeError):
                raise
            raise RuntimeError(f"Error downloading template: {str(e)}") from e
    
    @staticmethod
    def _get_auth_headers(github_token: Optional[str]) -> dict:
        """Get authorization headers for GitHub API.
        
        Args:
            github_token: Optional GitHub token
            
        Returns:
            Dict of headers (empty if no token)
        """
        if github_token:
            return {"Authorization": f"Bearer {github_token}"}
        return {}
    
    @staticmethod
    def extract(zip_path: Path, dest_path: Path) -> None:
        """Extract template zip file.
        
        Args:
            zip_path: Path to zip file
            dest_path: Destination directory
            
        Raises:
            RuntimeError: If extraction fails
        """
        try:
            dest_path.mkdir(parents=True, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(dest_path)
        
        except Exception as e:
            raise RuntimeError(f"Error extracting template: {str(e)}") from e
    
    @staticmethod
    def merge_settings(existing_path: Path, new_content: dict, verbose: bool = False) -> dict:
        """Merge JSON settings files.
        
        Performs a deep merge where:
        - New keys are added
        - Existing keys are preserved unless overwritten
        - Nested dictionaries are merged recursively
        - Lists and other values are replaced
        
        Args:
            existing_path: Path to existing JSON file
            new_content: New JSON content to merge
            verbose: Whether to print merge details
            
        Returns:
            Merged JSON content as dict
        """
        try:
            with open(existing_path, "r", encoding="utf-8") as f:
                existing_content = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # If file doesn't exist or is invalid, return new content
            return new_content
        
        merged = TemplateManager._deep_merge(existing_content, new_content)
        
        if verbose:
            console = Console()
            console.print(f"[cyan]Merged JSON file:[/cyan] {existing_path.name}")
        
        return merged
    
    @staticmethod
    def _deep_merge(base: dict, update: dict) -> dict:
        """Recursively merge update dict into base dict.
        
        Args:
            base: Base dictionary
            update: Dictionary to merge in
            
        Returns:
            Merged dictionary
        """
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = TemplateManager._deep_merge(result[key], value)
            else:
                result[key] = value
        return result
