from enum import Enum, auto
import os
from zipfile import ZipFile

import requests

__all__ = (
    'Target',
    'download_engine',
)


class Target(Enum):
    """Enumeration of supported Flutter targets."""

    #: Windows target.
    WINDOWS = auto()

    #: Linux target.
    LINUX = auto()

    #: macOS target.
    MACOS = auto()

    def get_download_url(self, version: str) -> str:
        """Retrieves the download URL for the Flutter engine.

        Parameters
        ----------
        version : str
            The engine version to download.

        Returns
        -------
        str
            The download URL.
        """

        if self == Target.WINDOWS:
            target = 'windows-x64/windows-x64-embedder.zip'
        elif self == Target.LINUX:
            target = 'linux-x64/linux-x64-embedder'
        elif self == Target.MACOS:
            target = 'darwin-x64/FlutterEmbedder.framework.zip'
        else:
            raise TypeError('Unsupported target')

        base_url = os.getenv(
            'FLUTTER_STORAGE_BASE_URL', 'https://storage.googleapis.com')

        return '{}/flutter_infra/flutter/{}/{}'.format(
            base_url, version, target)

    @property
    def library_name(self) -> str:
        """Returns the name of the Flutter library for the platform."""

        if self == Target.WINDOWS:
            return 'flutter_engine.dll'
        elif self == Target.LINUX:
            return 'libflutter_engine.so'
        elif self == Target.MACOS:
            return 'FlutterEmbedder.framework'
        else:
            raise TypeError('Unsupported target')

    @classmethod
    def get(cls) -> 'Target':
        """Determines the target platform to build for.
        
        This is solely driven by an environment variable called ``TARGET``.
        If the value contains``windows``, ``linux`` or ``apple``, the
        respective :class:`Target` member will be returned.

        Returns
        -------
        :class:`Target`
            The enum member corresponding to the target.

        Raises
        ------
        :exc:`ValueError`
            Raised when ``TARGET`` is not set at all or is set to an
            unknown target value.
        """

        target = os.getenv('TARGET')
        if target is None:
            raise ValueError('Cannot determine target')

        if 'windows' in target.lower():
            return cls.WINDOWS
        elif 'linux' in target.lower():
            return cls.LINUX
        elif 'apple' in target.lower():
            return cls.MACOS
        else:
            raise ValueError('Unknown target: {}'.format(target))


def unzip(file: str, destination: str):
    """Unzips a ZIP archive.

    Parameters
    ----------
    file : str
        Path to the archive to unzip.
    destination : str
        Path to the destination of the extracted content.
    """

    # Make sure the destination path exists.
    destination_parent, _ = os.path.split(destination)
    if not os.path.exists(destination_parent):
        os.makedirs(destination_parent)

    # Extract the archive.
    with ZipFile(file) as f:
        for name in f.namelist():
            f.extract(name, destination)


def download_engine(version: str, output: str):
    """Downloads the Flutter engine.

    This requires the ``TARGET`` environment variable so
    that :meth:`Target.download_url` knows what to download.

    Once the download is finished, it extracts the contents
    to a ```` directory.

    Parameters
    ----------
    version : str
        The engine version to download.
    output : str
        Path to the file where the result should be written.
    
    Raises
    ------
    :exc:`RuntimeError`
        Raised if the target architecture is unknown or the
        download of the engine resulted in a non-200 code.
    """

    # Make sure the specified path exists.
    output_parent, _ = os.path.split(output)
    if not os.path.exists(output_parent):
        os.makedirs(output_parent)
    
    # Determine the target.
    try:
        target = Target.get()
    except ValueError:
        raise RuntimeError(
            'Cannot retrieve the target.'
            'Please set the TARGET environment variable')
    
    # Download the engine and write the results to the output file.
    response = requests.get(target.get_download_url(version), stream=True)
    if response.status_code != 200:
        raise RuntimeError('Failed to download the Flutter engine')

    with open(output, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    
    # Extract the downloaded archive.
    unzip(output, output_parent)

    if target == Target.MACOS:
        # macOS download is a double zip file.
        library = target.library_name
        unzip(
            os.path.join(output_parent, library + '.zip'),
            os.path.join(output_parent, library)
        )
