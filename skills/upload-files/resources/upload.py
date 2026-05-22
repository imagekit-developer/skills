#!/usr/bin/env python3
"""CLI tool to upload files to ImageKit using the Upload API.

Requires:
    - IMAGEKIT_PRIVATE_KEY environment variable
    - requests library (pip install requests)

Usage:
    python upload.py <file_path> [options]

Examples:
    python upload.py image.jpg
    python upload.py image.jpg --folder /products --tags product,featured
    python upload.py image.jpg --file-name banner.jpg --folder /marketing --private
"""

import argparse
import json
import os
import sys
from pathlib import Path

import requests

UPLOAD_URL = "https://upload.imagekit.io/api/v1/files/upload"


def get_private_key():
    key = os.environ.get("IMAGEKIT_PRIVATE_KEY")
    if not key:
        print(
            "Error: IMAGEKIT_PRIVATE_KEY environment variable is not set.",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def upload_file(
    file_path: str,
    file_name: str = None,
    folder: str = "/",
    tags: list = None,
    is_private: bool = False,
    use_unique_name: bool = True,
    overwrite: bool = False,
    description: str = None,
    custom_coordinates: str = None,
):
    """Upload a local file to ImageKit via the Upload API."""
    private_key = get_private_key()
    path = Path(file_path)

    if not path.exists():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    if file_name is None:
        file_name = path.name

    files = {
        "file": (path.name, open(path, "rb")),
    }

    data = {
        "fileName": file_name,
        "folder": folder,
        "useUniqueFileName": str(use_unique_name).lower(),
        "isPrivateFile": str(is_private).lower(),
    }

    if tags:
        data["tags"] = ",".join(tags)

    if overwrite:
        data["overwriteFile"] = "true"
        data["useUniqueFileName"] = "false"

    if description:
        data["description"] = description

    if custom_coordinates:
        data["customCoordinates"] = custom_coordinates

    response = requests.post(
        UPLOAD_URL,
        files=files,
        data=data,
        auth=(private_key, ""),
    )

    if not response.ok:
        print(
            f"Error: Upload failed with status {response.status_code}", file=sys.stderr
        )
        print(response.text, file=sys.stderr)
        sys.exit(1)

    return response.json()


def main():
    parser = argparse.ArgumentParser(
        description="Upload files to ImageKit",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s image.jpg
  %(prog)s image.jpg --folder /products --tags product,featured
  %(prog)s image.jpg --file-name banner.jpg --overwrite
  %(prog)s video.mp4 --folder /videos --description "Product demo"
        """,
    )
    parser.add_argument("file", help="Path to the file to upload")
    parser.add_argument(
        "--file-name", help="Name for the uploaded file (default: original filename)"
    )
    parser.add_argument(
        "--folder", default="/", help="Destination folder in ImageKit (default: /)"
    )
    parser.add_argument("--tags", help="Comma-separated tags (e.g. product,featured)")
    parser.add_argument("--private", action="store_true", help="Mark file as private")
    parser.add_argument(
        "--no-unique-name",
        action="store_true",
        help="Don't add unique suffix to filename",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing file with same name",
    )
    parser.add_argument("--description", help="Description for the file")
    parser.add_argument("--custom-coordinates", help="Important area: x,y,width,height")
    parser.add_argument("--json", action="store_true", help="Output full JSON response")

    args = parser.parse_args()

    tags = args.tags.split(",") if args.tags else None

    result = upload_file(
        file_path=args.file,
        file_name=args.file_name,
        folder=args.folder,
        tags=tags,
        is_private=args.private,
        use_unique_name=not args.no_unique_name,
        overwrite=args.overwrite,
        description=args.description,
        custom_coordinates=args.custom_coordinates,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Upload successful!")
        print(f"  File ID:    {result['fileId']}")
        print(f"  Name:       {result['name']}")
        print(f"  URL:        {result['url']}")
        print(f"  Path:       {result['filePath']}")
        print(f"  Size:       {result['size']} bytes")
        print(f"  Type:       {result['fileType']}")
        if result.get("width"):
            print(f"  Dimensions: {result['width']}x{result['height']}")
        if result.get("thumbnailUrl"):
            print(f"  Thumbnail:  {result['thumbnailUrl']}")


if __name__ == "__main__":
    main()
