import os
from pathlib import Path

__all__ = (
    'get_flutter_version',
)


def read_version_from_sdk(path: str) -> str:
    """Reads the version from the Flutter SDK.
    
    Given the path to the SDK, the ``engine.version`` file located
    at ``{path}/bin/internal/engine.version`` will be used to read
    the version.

    .. warning::

        This function should not be called from user code.
        Use the safer and more universal implementation
        :func:`get_flutter_version` instead.

    Parameters
    ----------
    path : str
        Path to the Flutter SDK.
    
    Returns
    -------
    str
        The version string.
    """

    sdk_path = Path(path).joinpath('bin', 'internal')

    with open(str(sdk_path / 'engine.version'), encoding='utf-8') as f:
        return f.read().strip()


def get_flutter_version() -> str:
    """Retrieves the Flutter version.

    There are essentially three steps for looking up the version.
    As soon as one of them succeeds, the version will be returned.

    1. Check for the ``FLUTTER_ENGINE_VERSION`` environment variable
    and return its value, if set.

    2. Check for the ``FLUTTER_ROOT`` environment variable and call
    :func:`read_version_from_sdk` to read the version from the
    ``engine.version`` file.

    3. ``where.exe flutter`` on Windows and ``which flutter`` on
    UNIX will be used to get the SDK path to pass to
    :func:`read_version_from_sdk.`

    Returns
    -------
    str
        The version string.

    Raises
    ------
    :exc:`OSError`
        Raised when the version could not be retrieved.
    """

    # Attempt to read the version right away from the
    # `FLUTTER_ENGINE_VERSION` environment variable.
    version = os.getenv('FLUTTER_ENGINE_VERSION')
    if version is not None:
        return version

    # Check for the `FLUTTER_ROOT` environment variable
    # to read the version from the Flutter SDK.
    flutter_root = os.getenv('FLUTTER_ROOT')
    if flutter_root is not None:
        return read_version_from_sdk(flutter_root)

    # As a last resort, try to get the version through CLI
    # by guessing the path through `where.exe/which flutter`
    # and calling read_version_from_sdk with the resulting path.
    # TODO: Implement this.

    raise OSError('Failed to read the Flutter version') from None
