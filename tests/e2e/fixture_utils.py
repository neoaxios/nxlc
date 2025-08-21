"""Utilities for test fixture generation and management."""

import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional
import importlib.util

def get_nxlc_module():
    """
    Get the nxlc module, trying multiple strategies.
    
    Returns:
        The imported nxlc module
    
    Raises:
        ImportError: If nxlc cannot be found
    """
    # Strategy 1: Try direct import (if installed)
    try:
        import nxlc
        return nxlc
    except ImportError:
        pass
    
    # Strategy 2: Try importing from src directory
    try:
        # Add src to path temporarily
        src_path = Path(__file__).parent.parent.parent / 'src'
        if src_path.exists():
            sys.path.insert(0, str(src_path))
            try:
                import nxlc
                return nxlc
            finally:
                sys.path.pop(0)
    except ImportError:
        pass
    
    # Strategy 3: Use importlib to load from specific path
    possible_paths = [
        Path(__file__).parent.parent.parent / 'src' / 'nxlc.py',
        Path(__file__).parent.parent.parent / 'nxlc.py',
        Path.cwd() / 'src' / 'nxlc.py',
        Path.cwd() / 'nxlc.py',
    ]
    
    for nxlc_path in possible_paths:
        if nxlc_path.exists():
            spec = importlib.util.spec_from_file_location("nxlc", nxlc_path)
            if spec and spec.loader:
                nxlc = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(nxlc)
                return nxlc
    
    raise ImportError(
        "Could not find nxlc module. Ensure it's installed or available in src/"
    )


def get_language_definitions() -> Dict[str, Any]:
    """
    Get language definitions from nxlc module.
    
    Returns:
        Dict with 'languages' and 'comment_patterns' keys
    """
    nxlc = get_nxlc_module()
    
    # Access the language definitions directly from the module
    language_defs = nxlc.LanguageDefinitions()
    
    return {
        'languages': language_defs.LANGUAGE_EXTENSIONS,
        'comment_patterns': language_defs.COMMENT_PATTERNS
    }


def find_project_root() -> Path:
    """
    Find the project root directory by looking for marker files.
    
    Returns:
        Path to project root
    
    Raises:
        FileNotFoundError: If project root cannot be determined
    """
    current = Path(__file__).resolve().parent
    
    # Look for project markers (prioritize specific project files)
    # Check for pyproject.toml or setup.py first (more specific than README.md)
    specific_markers = ['pyproject.toml', 'setup.py']
    general_markers = ['.git', 'README.md']
    
    for _ in range(5):  # Max 5 levels up
        # First check for specific Python project markers
        if any((current / marker).exists() for marker in specific_markers):
            return current
        # Then check if we have BOTH .git and README.md (more likely to be root)
        if all((current / marker).exists() for marker in general_markers):
            return current
        parent = current.parent
        if parent == current:  # Reached filesystem root
            break
        current = parent
    
    # If not found, use the traditional parent.parent.parent approach
    # This maintains backward compatibility
    fallback = Path(__file__).parent.parent.parent
    if (fallback / 'src' / 'nxlc.py').exists():
        return fallback
    
    raise FileNotFoundError(
        "Could not find project root. Looking for: " + ", ".join(markers)
    )


def get_nxlc_executable() -> Path:
    """
    Get the path to the nxlc executable/script.
    
    Returns:
        Path to nxlc executable
    
    Raises:
        FileNotFoundError: If nxlc executable cannot be found
    """
    # Try multiple strategies
    strategies = [
        # 1. Check if nxlc is in PATH (installed via pip)
        lambda: Path(os.popen('which nxlc').read().strip()),
        
        # 2. Check common locations relative to project root
        lambda: find_project_root() / 'src' / 'nxlc.py',
        lambda: find_project_root() / 'nxlc.py',
        lambda: find_project_root() / 'bin' / 'nxlc',
        
        # 3. Check virtual environment
        lambda: Path(sys.prefix) / 'bin' / 'nxlc',
        lambda: Path(sys.prefix) / 'Scripts' / 'nxlc.exe',  # Windows
    ]
    
    for strategy in strategies:
        try:
            path = strategy()
            if path and path.exists():
                return path
        except:
            continue
    
    raise FileNotFoundError(
        "Could not find nxlc executable. Ensure it's installed or in src/"
    )


# Configuration class for centralized settings
class TestConfig:
    """Centralized configuration for test utilities."""
    
    def __init__(self):
        self._project_root = None
        self._nxlc_path = None
        self._fixture_dir = None
    
    @property
    def project_root(self) -> Path:
        """Get cached project root."""
        if self._project_root is None:
            self._project_root = find_project_root()
        return self._project_root
    
    @property
    def nxlc_path(self) -> Path:
        """Get cached nxlc executable path."""
        if self._nxlc_path is None:
            self._nxlc_path = get_nxlc_executable()
        return self._nxlc_path
    
    @property
    def fixture_dir(self) -> Path:
        """Get fixture directory."""
        if self._fixture_dir is None:
            self._fixture_dir = self.project_root / 'tests' / 'e2e' / 'fixtures'
        return self._fixture_dir
    
    @classmethod
    def from_env(cls) -> 'TestConfig':
        """
        Create config from environment variables.
        
        Environment variables:
            NXLC_PROJECT_ROOT: Override project root detection
            NXLC_EXECUTABLE: Override nxlc executable path
            NXLC_FIXTURE_DIR: Override fixture directory
        """
        config = cls()
        
        if 'NXLC_PROJECT_ROOT' in os.environ:
            config._project_root = Path(os.environ['NXLC_PROJECT_ROOT'])
        
        if 'NXLC_EXECUTABLE' in os.environ:
            config._nxlc_path = Path(os.environ['NXLC_EXECUTABLE'])
        
        if 'NXLC_FIXTURE_DIR' in os.environ:
            config._fixture_dir = Path(os.environ['NXLC_FIXTURE_DIR'])
        
        return config


# Global config instance
config = TestConfig.from_env()