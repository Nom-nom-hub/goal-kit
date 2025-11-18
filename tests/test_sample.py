"""Sample test file to verify testing infrastructure is working."""

import pytest


class TestSample:
    """Sample tests to verify pytest is configured correctly."""

    def test_sample_pass(self):
        """A simple passing test."""
        assert 1 + 1 == 2

    def test_sample_with_fixture(self, temp_project_dir):
        """A test that uses a fixture."""
        assert temp_project_dir.exists()
        assert temp_project_dir.is_dir()

    @pytest.mark.unit
    def test_sample_unit(self):
        """Sample unit test."""
        value = 42
        assert value == 42

    @pytest.mark.integration
    def test_sample_integration(self, git_repo):
        """Sample integration test."""
        assert git_repo.exists()
        assert (git_repo / ".git").exists()

    def test_helpers_available(self, test_helpers):
        """Test that helper methods are available."""
        assert hasattr(test_helpers, "create_goal_directory")
        assert hasattr(test_helpers, "create_goal_file")
        assert hasattr(test_helpers, "assert_goal_structure")
