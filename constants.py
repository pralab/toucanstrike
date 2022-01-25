PADDING = 'padding'
EXTEND = 'extend'
SHIFT = 'shift'
FULL_DOS = 'full_dos'
PARTIAL_DOS = 'partial_dos'
HEADER_FIELDS = 'header_fields'
GAMMA_PADDING = 'gamma_padding'
GAMMA_SECTIONS = 'gamma_sections'
MALCONV = 'malconv'
EMBER_GBDT = 'ember_gbdt'
SOREL_NET = 'sorel_dnn'

ALL_MODELS = [MALCONV, EMBER_GBDT, SOREL_NET]
ERROR_PROMPT = "(＃＞＜) "
SUCCESS_PROMPT = "(o^▽^o) "
INFO_PROMPT = "__φ(．．) "
CRASH_PROMPT = "(╯°□°）╯︵ ┻━┻ "
SEPARATOR_PROMPT = "(((o(*°▽°*)o)))"
TOUCANSTRIKE_DEFAULT_PROMPT = "toucanstrike> "

BYTE_ATTACKS = [PARTIAL_DOS, FULL_DOS, SHIFT, EXTEND, PADDING, HEADER_FIELDS]
GAMMA_ATTACKS = [GAMMA_PADDING, GAMMA_SECTIONS]
WB_TARGETS = [MALCONV]

TOUCAN_STRIKE_COMMANDS = "ToucanStrike Commands"
banner = """
████████╗ ██████╗ ██╗   ██╗ ██████╗ █████╗ ███╗   ██╗███████╗████████╗██████╗ ██╗██╗  ██╗███████╗
╚══██╔══╝██╔═══██╗██║   ██║██╔════╝██╔══██╗████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝
   ██║   ██║   ██║██║   ██║██║     ███████║██╔██╗ ██║███████╗   ██║   ██████╔╝██║█████╔╝ █████╗  
   ██║   ██║   ██║██║   ██║██║     ██╔══██║██║╚██╗██║╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  
   ██║   ╚██████╔╝╚██████╔╝╚██████╗██║  ██║██║ ╚████║███████║   ██║   ██║  ██║██║██║  ██╗███████╗
   ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝                                                                                         
"""
