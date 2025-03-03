## Base64 Codec

This plugin provides tools for encoding and decoding Base64 specified
in [RFC 4648](https://datatracker.ietf.org/doc/html/rfc4648.html). It supports text as input, while text or image files
as output.

### Description

| Tool                 | Purpose                                     | Input                                                                                               | Output                |
|----------------------|---------------------------------------------|-----------------------------------------------------------------------------------------------------|-----------------------|
| base64_encoder       | Encodes data to Base64 format               | Raw text                                                                                            | Base64 encoded string |
| base64_decoder       | Decodes Base64 encoded data                 | Base64 encoded string                                                                               | Raw text              |
| base64_image_decoder | Decodes Base64 encoded string to image file | Base64 encoded string, starting with prefixes for png, jpeg, webp, svg, eg. `data:image/png;base64` | Image file            |