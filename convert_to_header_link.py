NON_SPECIAL_CHARARCTERS = list("0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM#- ")

def convert_to_header_link(header: str) -> str:
    header_level: int = len(header) - len(header.lstrip("#"))
    header = header.lstrip("#").strip()
    new_header: list[str] = []
    for char in header:
        if char in NON_SPECIAL_CHARARCTERS:
            new_header.append(char)
    
    return f"{'#' * header_level}{''.join(new_header).lower().replace(' ', '-')}"

if __name__ == "__main__":
    print(convert_to_header_link(input("Enter a header to convert: ")))