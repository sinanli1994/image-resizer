from __future__ import annotations

from io import BytesIO
from pathlib import Path

from PIL import Image

SUPPORTED_OUTPUT_FORMATS = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
    ".webp": "WEBP",
}

QUALITY_ADJUSTABLE_FORMATS = {"JPEG", "WEBP"}


def resize_and_compress(
    input_path: str,
    output_path: str,
    width: int | None = None,
    height: int | None = None,
    quality: int = 100,
    keep_aspect_ratio: bool = True,
    target_size_bytes: int | None = None,
) -> str:
    """
    Resize and compress an image using Pillow.

    Returns the output image path.
    """
    src = Path(input_path)
    dst = Path(output_path)

    if not src.exists():
        raise FileNotFoundError(f"Input image not found: {src}")

    if (width is None) != (height is None):
        raise ValueError("Width and height must both be set when resizing is enabled.")
    if width is not None and width <= 0:
        raise ValueError("Width must be greater than zero.")
    if height is not None and height <= 0:
        raise ValueError("Height must be greater than zero.")
    if target_size_bytes is not None and target_size_bytes <= 0:
        raise ValueError("Target file size must be greater than zero.")
    if dst.suffix.lower() not in SUPPORTED_OUTPUT_FORMATS:
        supported = ", ".join(sorted(SUPPORTED_OUTPUT_FORMATS))
        raise ValueError(f"Unsupported output format. Use one of: {supported}.")

    quality = max(1, min(100, quality))
    dst.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(src) as img:
        if width is not None and height is not None:
            if keep_aspect_ratio:
                img.thumbnail((width, height), Image.Resampling.LANCZOS)
            else:
                img = img.resize((width, height), Image.Resampling.LANCZOS)

        output_format = SUPPORTED_OUTPUT_FORMATS[dst.suffix.lower()]
        prepared_img = _prepare_image_for_format(img, output_format)

        if target_size_bytes is not None:
            encoded = _encode_to_target_size(
                img=prepared_img,
                output_format=output_format,
                target_size_bytes=target_size_bytes,
                max_quality=quality,
            )
            dst.write_bytes(encoded)
        else:
            save_kwargs = _build_save_kwargs(output_format, quality)
            prepared_img.save(dst, format=output_format, **save_kwargs)

    return str(dst)


def _encode_to_target_size(
    img: Image.Image,
    output_format: str,
    target_size_bytes: int,
    max_quality: int,
) -> bytes:
    if output_format not in QUALITY_ADJUSTABLE_FORMATS:
        raise ValueError(
            "Target file size is supported only for JPEG and WEBP output."
        )

    best_data: bytes | None = None

    for quality in range(max_quality, 0, -1):
        encoded = _encode_image(img, output_format, quality, for_target=True)
        if len(encoded) <= target_size_bytes:
            best_data = encoded
            break

    if best_data is None:
        smallest = _encode_image(img, output_format, 1, for_target=True)
        if len(smallest) > target_size_bytes:
            raise ValueError(
                "Target file size could not be reached. Try a larger target, "
                "enable dimension limits, or choose a different format."
            )
        return smallest

    return best_data


def _encode_image(
    img: Image.Image,
    output_format: str,
    quality: int,
    for_target: bool = False,
) -> bytes:
    buffer = BytesIO()
    img.save(
        buffer,
        format=output_format,
        **_build_save_kwargs(output_format, quality, for_target),
    )
    return buffer.getvalue()


def _build_save_kwargs(
    output_format: str,
    quality: int,
    for_target: bool = False,
) -> dict[str, object]:
    save_kwargs: dict[str, object] = {"optimize": not for_target}
    if output_format in QUALITY_ADJUSTABLE_FORMATS:
        save_kwargs["quality"] = quality
    if output_format == "JPEG" and for_target:
        # Use the least aggressive JPEG compression path so the result can get
        # as close as possible to the requested file size.
        save_kwargs["subsampling"] = 0
    if output_format == "WEBP" and for_target:
        save_kwargs["method"] = 0
    return save_kwargs


def _prepare_image_for_format(img: Image.Image, output_format: str) -> Image.Image:
    if output_format == "JPEG":
        return _to_jpeg_safe_image(img)
    if output_format == "PNG" and img.mode == "P" and "transparency" in img.info:
        return img.convert("RGBA")
    return img.copy()


def _to_jpeg_safe_image(img: Image.Image) -> Image.Image:
    if "A" in img.getbands():
        base = Image.new("RGB", img.size, (255, 255, 255))
        base.paste(img.convert("RGBA"), mask=img.getchannel("A"))
        return base
    if img.mode != "RGB":
        return img.convert("RGB")
    return img.copy()
