from .pandai import parse_pandai
from .callisto import parse_callisto

# Registry mapping channel IDs to parser functions
PARSER_REGISTRY = {
    2166348331: parse_pandai,  # Pandai Trading Signal VIP
    1623437581: parse_callisto,  # CallistoFx Premium Channel
}
