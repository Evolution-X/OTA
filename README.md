### JSON structure ###
```
{
  "response": [
    {
      "maintainer": "Name (nickname)",
      "currently_maintained": true/false,
      "oem": "OEM",
      "device": "Device Name",
      "filename": "EvolutionX-16.0-<date>-<device codename>-v<evolution_x_version>.zip",
      "download": "https://cdn.evolution-x.org/<device codename>/14/EvolutionX-15.0-<date>-<device codename>-v<evolution_x_version>.zip/download",
      "timestamp": 0000000000,
      "md5": "abcdefg123456",
      "sha256": "abcdefg123456",
      "size": 123456789,
      "version": "<evolution_x_version>",
      "buildtype": "user/userdebug/eng",
      "forum": "https://forum link", #(mandatory)
      "firmware": "https://firmware link",
      "paypal": "https://donation link",
      "github": "GitHub Username",
      "initial_installation_images": [
        "img files to be flashed before sideloading Evolution X's zip"
      ]
      "extra_images": [
        "Additional img files that can be flashed"
      ]
    }
  ]
}
```
