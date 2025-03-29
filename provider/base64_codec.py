from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

from tools.base64_decoder import Base64TextDecodeTool
from tools.base64_encoder import Base64TextEncodeTool
from tools.base64_image_decoder import Base64ImageDecodeTool


class Base64CodecProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        try:
            """
            IMPLEMENT YOUR VALIDATION HERE
            """
            Base64TextEncodeTool.from_credentials({})
            Base64TextDecodeTool.from_credentials({})
            Base64ImageDecodeTool.from_credentials({})
        except Exception as e:
            raise ToolProviderCredentialValidationError(str(e))
