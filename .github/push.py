import requests
from datetime import datetime
import os
import sys
import json

file_path = sys.argv[1]

bka_webhook = os.environ["BKA_WEBHOOK"]
udc_webhook = os.environ["UDC_WEBHOOK"]
udc_vanilla_webhook = os.environ["UDC_VANILLA_WEBHOOK"]
bka_vanilla_webhook = os.environ["BKA_VANILLA_WEBHOOK"]
vic_webhook = os.environ["VIC_WEBHOOK"]
vic_vanilla_webhook = os.environ["VIC_VANILLA_WEBHOOK"]

def get_commit_hash(branch, codename):
    path = f"changelogs/{codename}.txt"
    api_url = f"https://api.github.com/repos/Evolution-X/OTA/commits?path={path}&sha={branch}"
    response = requests.get(api_url)
    response.raise_for_status()
    commits = response.json()
    if commits:
        return commits[0]['sha']
    else:
        return "Unknown"

def parse_device():
    with open(file_path) as f:
        codename = f.name.split("/")[-1].split(".")[0]
        data = json.load(f)
        response = data["response"]
        filename = response[0]["filename"]
        oem = response[0]["oem"]
        device = response[0]["device"]
        maintainer = response[0]["maintainer"]
        version = response[0]["version"]
        build_date = response[0]["timestamp"]
        file_size = response[0]["size"]
        download_link = response[0]["download"]
        xda_thread = response[0]["forum"]
        github = response[0]["github"]
    return filename, codename, oem, device, maintainer, version, build_date, file_size, download_link, xda_thread, github

def humanize(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def webhook_send():
    filename, codename, oem, device, maintainer, version, build_date, file_size, download_link, xda_thread, github = parse_device()
    
    # Extract only the branch name from GITHUB_REF, default to 'vic'
    branch = os.environ.get("GITHUB_REF", "refs/heads/vic").split("/")[-1]
    commit_hash = get_commit_hash(branch, codename)
    
    if "Vanilla" in filename and "11." in version:
        webhook_url = bka_vanilla_webhook
    if "Vanilla" in filename and "10." in version:
        webhook_url = vic_vanilla_webhook
    if "Vanilla" in filename and "9." in version:
        webhook_url = udc_vanilla_webhook
    if "Vanilla" not in filename and "11." in version:
        webhook_url = bka_webhook
    if "Vanilla" not in filename and "10." in version:
        webhook_url = vic_webhook
    if "Vanilla" not in filename and "9." in version:
        webhook_url = udc_webhook

    has_xda_thread = xda_thread and xda_thread != "null" and xda_thread.strip() != ""
    
    if "Vanilla" in filename:
        color = 0xffe7c4
    else:
        color = 0x2986cc
    evo_org_tumbnail = f"https://raw.githubusercontent.com/Evolution-X/www_gitres/refs/heads/main/devices/images/{codename}.webp"
    if requests.get(evo_org_tumbnail).status_code == 404:
        thumbnail = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7DK6a--HvqADA_u3mGjXSVUvxxZ5sw3x9Sw&s"
    else:
        thumbnail = evo_org_tumbnail
    
    # Prepare main description
    description = f"""
            📲 • New build available for **{oem} {device}** ({codename})
            👤 • **By [{maintainer}](https://github.com/{github})**\n
            📦 • **Version**: {version}
            🕒 • **Build date**: {datetime.fromtimestamp(build_date, tz=None).date()}
            📎 • **Build size**: {humanize(file_size)}
            🗞️ • **[Changelog](https://raw.githubusercontent.com/Evolution-X/OTA/{commit_hash}/changelogs/{codename}.txt)**
            <:Evo:670530693985730570> • **Check [device's infos](https://evolution-x.org/devices/{codename}) directly on our website!**\n
            
            ⬇️ [Download link]({download_link}) ⬇️\n"""
    
    # Add XDA Thread section only if there's a valid link
    if has_xda_thread:
        description += f" \n🌐 [XDA Thread]({xda_thread}) 🌐"
    
    data = {
        "embeds": [
    {
            "type": "rich",
            "description": description,
            "image": {
                "url": "https://wiki.evolution-x.org/keepevolving.png"
            },
            "color": f"{color}",
            "thumbnail": {
                "url": f"{thumbnail}"
                },
            "author": {
                "name": f"New build available !",
                "icon_url": f"https://github.com/{github}.png"
                },
            "timestamp": datetime.now().isoformat(),
            "footer": {
                "text": "Evolution X",
                "icon_url": "https://avatars.githubusercontent.com/u/165590896?s=200&v=4"
            }}]
    }

    result = requests.post(webhook_url, json=data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
    else:
        print("Payload delivered successfully, code {}.".format(result.status_code))


webhook_send()

