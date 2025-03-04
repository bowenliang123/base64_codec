## Base64 Codec

Author: [bowenliang123](https://github.com/bowenliang123)

This plugin provides tools for encoding and decoding Base64 specified
in [RFC 4648](https://datatracker.ietf.org/doc/html/rfc4648.html). It supports text as input, while text or image files
as output.

### Description

| Tool                 | Input                                                                                                    | Output                |
|----------------------|----------------------------------------------------------------------------------------------------------|-----------------------|
| base64_encoder       | Raw text                                                                                                 | Base64 encoded string |
| base64_decoder       | Base64 encoded string                                                                                    | Raw text              |
| base64_image_decoder | Base64 encoded string of PNG, JPG, WEBP, SVG format, starting with prefixes, eg. `data:image/png;base64` | Image file            |

- base64_encoder

  <img src="./_assets/snapshot1.png" width="100%" >

- base64_decoder

  <img src="./_assets/snapshot2.png" width="100%" >

- base64_image_decoder

  <img src="./_assets/snapshot3.png" width="100%" >
