## Base64 Codec

Author: [bowenliang123](https://github.com/bowenliang123)

This plugin provides tools for encoding and decoding Base64 specified
in [RFC 4648](https://datatracker.ietf.org/doc/html/rfc4648.html). It supports text as input, while text or image files
as output.

### Description

| Tool                 | Input                                                    | Output                |
|----------------------|----------------------------------------------------------|-----------------------|
| base64_encoder       | Raw text                                                 | Base64 encoded string |
| base64_decoder       | Base64 encoded text                                      | Raw text              |
| base64_image_encoder | Image file                                               | Base64 encoded text   |
| base64_image_decoder | Base64 encoded text of PNG, JPG, WEBP, SVG format prefix | Image file            |

- base64_encoder

  ![](_assets/snapshot1.png)

- base64_decoder

  ![](_assets/snapshot2.png)

- base64_image_encoder
   
  ![](_assets/snapshot4.png)

- base64_image_decoder

  ![](_assets/snapshot3.png)
