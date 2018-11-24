from collections import namedtuple
ProjectInfo = namedtuple("ProjectInfo", "name channel_id url")

def get_by_name(project: str, all_links: [ProjectInfo]) -> [ProjectInfo]:
    links = []
    for pinfo in all_links:
        if project.lower() in pinfo.name.lower():
            links.append(pinfo)
    return links

def get_by_channel(channel: str, all_links: [ProjectInfo]) -> [ProjectInfo]:
    links = []
    for pinfo in all_links:
        if channel == pinfo.channel_id:
            links.append(pinfo)
    return links